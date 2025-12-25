import asyncio
import json
from os import fspath
from sys import executable
from typing import Iterator, List, Optional, Tuple, Union

import d_ast_parse
import d_ast_pretty
import d_grammar_expand
import p_consts
import p_data_structures as pds
import p_generator
import p_generator_lw
import p_grammar
import p_llm_gen
import p_rule_applicator as prapp
import p_ext_rule_chooser
import p_rule_inferencer
import p_rule_validator
import p_ruleset
import p_subject
import p_translators
import p_tree_log as ptlog
import p_utils
import p_visitor as pvis
import p_visitor_js as pvjs
import p_visitor_py as pvpy
from p_config import Config


_EOT_MODULE_TEMPLATE = '''from os import chdir
def myexactlog(*args, **kwargs): pass
chdir({!r})
{}
'''

logger = p_utils.setup_logger(__name__)


class ProbNode_NoTRule_AllTSPsExhaustedError(RuntimeError): pass
class TSP_NoTRuleLearnedError(RuntimeError): pass
class CouldNotGenRefTranslationsError(RuntimeError): pass
class _ValidationError_ProblematicNodeExists(RuntimeError): pass
class TestFunctionGenerationError(RuntimeError): pass
class NoTSPsGeneratedError(RuntimeError): pass
class PartialProgramGenerationError(RuntimeError): pass
class BypassStaRuleLearningError(RuntimeError): pass


def _get_pre_context_global(
  src_main_code: str,
  stat_npath: List[int]
) -> str:
  '''
  A pre-context is part of the code that appears before the context node
  of the problematic node inside a function body.

  The goal of this function is to extract pre-context for the snippet
  that is used to validate the translation rule. The idea of extraction
  algorithm is to find the enclosing `function_definition`s `block` node,
  and remove all nodes that appear after the context node. What is left
  is the pre-context that we need. After that, we replace the context
  node with a special identifier, that is later string-replaced by the
  actual snippet.
  '''
  def _process_elif_clauses(else_clause_node: pvpy.ElifClauseNode) -> None:
    '''
    Replace all children of `elif` clause's body with a pass statement.
    '''
    pass_statement_node = pvpy.PassStatementNode.build()
    else_clause_node.consequence.children = [pass_statement_node]
    pass_statement_node.set_parent(else_clause_node.consequence)

  def _process_else_clauses(else_clause_node: pvpy.ElseClauseNode) -> None:
    '''
    Replace all children of `else` clause's body with a pass statement.
    '''
    pass_statement_node = pvpy.PassStatementNode.build()
    else_clause_node.body.children = [pass_statement_node]
    pass_statement_node.set_parent(else_clause_node.body)

  def _process_except_clause(except_clause_node: pvpy.ExceptClauseNode) -> None:
    '''
    Replace all children of `except` clause's body with a pass statement.
    '''
    pass_statement_node = pvpy.PassStatementNode.build()
    except_clause_body = except_clause_node.get_nt_children()[-1]
    except_clause_body.children = [pass_statement_node]
    pass_statement_node.set_parent(except_clause_body)

  tree = pvpy.Tree.from_str(src_main_code)
  statement_node = tree.root_node.get_child_by_path(stat_npath)

  # 1. find the enclosing function_definition node's block
  cursor_node = statement_node
  while cursor_node.get_parent() is not None:

    # remove siblings to the right of cursor_node as we are moving up
    next_sibling = cursor_node.next_sibling()

    while next_sibling is not None:
      # need to get the pointer to the next_sibling++
      # before removing next_sibling itself
      next_next_sibling = next_sibling.next_sibling()

      # keep elif and else clauses because they are part of the translation rule
      # they are part of the translation rule due to the fact that
      # they are not simplified. Refer to p_grammar.simplify_template() for more information.
      if isinstance(next_sibling, pvpy.ElifClauseNode):
        _process_elif_clauses(next_sibling)
        next_sibling = next_next_sibling
        continue
      if isinstance(next_sibling, pvpy.ElseClauseNode):
        _process_else_clauses(next_sibling)
        next_sibling = next_next_sibling
        continue
      if isinstance(next_sibling, pvpy.ExceptClauseNode):
        _process_except_clause(next_sibling)
        next_sibling = next_next_sibling
        continue

      next_sibling.get_parent().get_children().remove(next_sibling)
      next_sibling.parent = None
      next_sibling = next_next_sibling

    # move up the tree
    cursor_node = cursor_node.get_parent()
    if isinstance(cursor_node, pvpy.BlockNode):
      if isinstance(cursor_node.get_parent(), pvpy.FunctionDefinitionNode):
        break

  # 2. replace the context node with a special identifier
  spec_id_stat = pvpy.ExpressionStatementNode.build(
    pvpy.IdentifierNode.build(p_consts.PRE_CTX_SPEC_IDENT))
  spec_id_stat.set_parent(statement_node.get_parent())
  context_node_idx_as_child = statement_node.parent.children.index(statement_node)
  statement_node.parent.children[context_node_idx_as_child] = spec_id_stat

  # 3. pretty print the block
  pp = pvpy.PrettyPrinter(indent_with='    ')
  pp.visit(cursor_node)
  pre_context = '\n'.join(pp.lines)
  return pre_context


def _get_pre_context_eot(
  src_program: str,
  stat_npath: list[int],
  npath_blacklist: list[list[int]],
) -> str:
  '''Return the context of the statement to be translated.

  Nodes blacklisted are to be translated after this statement
  in execution-order translation, so that only the pre-context is left.
  '''
  root_node = pvpy.Tree.from_str(src_program).root_node
  for npath in npath_blacklist:
    if npath[:len(stat_npath)] == stat_npath:
      continue  # keep ancestors of the statement to be translated
    node = root_node.get_child_by_path(npath)
    assert node is not None
    if isinstance(node, pvpy.ElseClauseNode):
      node.body.children = []
    elif isinstance(node, pvpy.ElifClauseNode):
      node.consequence.children = []
    else:
      node.parent.children.remove(node)

  stack = [root_node]
  while stack:
    node = stack.pop()
    if isinstance(node, pvpy.BlockNode) and not node.children:
      pass_statement_node = pvpy.PassStatementNode.build()
      node.children = [pass_statement_node]
      pass_statement_node.set_parent(node)
    stack.extend(node.children)

  statement_node = root_node.get_child_by_path(stat_npath)
  assert statement_node is not None
  spec_id_stat = pvpy.ExpressionStatementNode.build(
    pvpy.IdentifierNode.build(p_consts.PRE_CTX_SPEC_IDENT))
  spec_id_stat.set_parent(statement_node.get_parent())
  context_node_idx_as_child = statement_node.parent.children.index(statement_node)
  statement_node.parent.children[context_node_idx_as_child] = spec_id_stat
  return pvpy.PrettyPrinter(indent_with='    ').visit(root_node)


def get_pre_context(
  src_main_code: str,
  lang: str,
  is_three_split: bool,
  stat_nid: int,
  nid_blacklist: list[int],
) -> str:
  '''
  Get pre-context for the statement node.
  The pre-context is the code that appears before the statement node
  in the source code up to the closest enclosing function definition.
  '''
  # p_utils.log_json_time(f'args-get_pre_context.json', locals())
  tree = pds.PirelTree.from_code_str(src_main_code, lang)
  root_node = tree.get_root_node()
  stat_node = root_node.get_node_by_id(stat_nid)
  stat_npath = root_node.get_path_to_child(stat_node)
  if is_three_split:
    return _get_pre_context_global(src_main_code, stat_npath)
  else:
    blacklist = sorted(map(root_node.get_path_to_child,
                           map(root_node.get_node_by_id, nid_blacklist)),
                       reverse=True)
    return _get_pre_context_eot(src_main_code, stat_npath, blacklist)


def _can_be_context_node(
  node: pds.PirelNode,
  lang: str
) -> bool:
  '''
  A node is a context node if AST of its text,
  when parsed on its own, is isomorphic to itself.
  Refer to p_templates._validate_template() for more information.
  '''
  # must be non-terminal
  if node.is_terminal():
    return False
  # node text must not have errors when parsed as it is
  if p_utils.does_have_parse_error(node.get_text(), lang):
    return False
  # parse the node text as a program on its own
  ast_text, ast_ann = d_ast_parse.parse_text_dbg(node.get_text(), lang, keep_text=True)
  tree = pds.PirelTree(ast_text, ast_ann)
  # there should be exactly one context node
  if len(tree.get_root_node().get_children()) != 1:
    return False
  context_node = tree.get_root_node().get_children()[0]
  # context node must be isomorphic to the original node
  if not node.is_type_isomorphic_to(context_node):
    return False
  return True


def _check_needs_rec_rule_learning_directly(
  templates_dict: dict
) -> bool:
  '''
  Check template_origin to see if we need to bypass standard rule learning
  and go directly to recovery rule learning.
  '''

  def __pattern_1_type_fn_three_args(template_origin: str) -> bool:
    '''
    Assignment statements of the form:
    Clz = type(class_name, (super_class,), {...})
    '''
    ts_query_str = '(module (expression_statement (assignment left: (identifier) right: (call function: (identifier) @name arguments: (argument_list "(" (_) "," (_) "," (_) ")" ) ) ) ) )'
    tree = p_consts._py_parser.parse(bytes(template_origin, 'utf8'))
    ts_query = p_consts._py_language.query(ts_query_str)
    captures = ts_query.captures(tree.root_node)
    if len(captures) != 1:
      return False
    capture, _ = captures[0]
    fn_name = template_origin[capture.start_byte:capture.end_byte]
    if fn_name != 'type':
      return False
    logger.debug('Matched direct recovery learning pattern: type() with three arguments')
    return True

  # in cases when templates_dict is loaded from str, keys are strings
  _valid_template_idx = p_utils.to_int(templates_dict['num_templates']) - 1
  template_dict = templates_dict.get(_valid_template_idx) or templates_dict.get(str(_valid_template_idx))

  patterns = [
    __pattern_1_type_fn_three_args,
  ]
  for pattern in patterns:
    if pattern(template_dict['template_origin']):
      logger.debug('Bypassing standard rule learning: matched a direct recovery learning pattern')
      return True
  return False


def _visitor_nodes_with_pirel_id_instrumentation(
  visitor_nodes: list[pvis.AbstractNode],
  pirel_nodes: list[pds.PirelNode],
  lang: str,
) -> Iterator[pvis.AbstractNode]:
  assert len(visitor_nodes) == len(pirel_nodes), breakpoint()
  for visitor_node, pirel_node in zip(visitor_nodes, pirel_nodes):
    if (_can_be_context_node(pirel_node, lang)
        and pirel_node.get_ts_node_type() != 'function_definition'):
      print_stmt = f"print('PiREL', {pirel_node.get_id()})"
      print_node, = pvpy.Tree.from_str(print_stmt).root_node.children
      yield print_node
    yield visitor_node


def _instrument_visitor_node_with_pirel_node_id(
  visitor_node: pvis.AbstractNode,
  pirel_node: pds.PirelNode,
  lang: str,
) -> None:
  if isinstance(visitor_node, pvpy.StringNode):
    return  # FIXME: handle f-strings (short circuit here can be kept though)
  visitor_children = visitor_node.children
  pirel_children = pirel_node.get_children()
  children = list(_visitor_nodes_with_pirel_id_instrumentation(
    visitor_children, pirel_children, lang))
  assert len(visitor_children) == len(pirel_children)
  for visitor_child, pirel_child in zip(visitor_node.children,
                                        pirel_node.get_children()):
    _instrument_visitor_node_with_pirel_node_id(visitor_child,
                                                pirel_child, lang)
  visitor_node.children = children


async def get_statement_nodes_eot(
  src_program: str,
  lang: str,
  return_node_ids: bool = False,
) -> list[pds.PirelNode|int]:
  '''
  Return a list of statement nodes for execution-order translation.

  If node identifiers are requested, skip finding the PiREL nodes
  from their ID, which is costly.
  '''
  workdir = fspath(p_consts.BENCHMARK_CONFIGS['skel']['benchmark_dir'])  # FIXME
  pirel_root_node = pds.PirelTree.from_code_str(src_program,
                                                lang).get_root_node()
  visitor_root_node = pvpy.Tree.from_str(src_program).root_node
  _instrument_visitor_node_with_pirel_node_id(visitor_root_node,
                                              pirel_root_node, lang)
  module = pvpy.PrettyPrinter(indent_with='    ').visit(visitor_root_node)
  module = _EOT_MODULE_TEMPLATE.format(workdir, module)

  logger.debug('Prepared instrumented module for EoT statement node extraction.')
  p_utils.log_file_time('src_instrumented_eot.py', module)

  proc = await asyncio.create_subprocess_exec(
    executable, '-c', module,
    stdout=asyncio.subprocess.PIPE,
    stderr=asyncio.subprocess.PIPE
  )
  stdout = (await proc._read_stream(1)).decode()
  stderr = (await proc._read_stream(2)).decode()
  await proc.wait()
  assert proc.returncode == 0, f'Error executing instrumented module:\n{stderr}'

  nodes, visited = [], set()
  for line in stdout.splitlines():
    if line.startswith('PiREL '):
      node_id = int(line.removeprefix('PiREL '))
      if node_id not in visited:
        visited.add(node_id)
        nodes.append(node_id if return_node_ids
                     else pirel_root_node.get_node_by_id(node_id))
  return nodes


async def _get_statement_nodes(
  src_main_code: str,
  lang: str,
  is_three_split: bool,
  return_node_ids: bool = False,
) -> List[Union[pds.PirelNode, int]]:
  '''
  Statement nodes are primary units of code in the source code.
  In other words, a source code is a sequence of statement nodes.
  '''
  if not is_three_split:
    return await get_statement_nodes_eot(src_main_code, lang, return_node_ids)

  def __rec_pre_order(node: pds.PirelNode, lang: str) -> None:
    nonlocal nodes
    if _can_be_context_node(node, lang):
      nodes.append(node)
    for child in node.get_children():
      __rec_pre_order(child, lang)

  tree = pds.PirelTree.from_code_str(src_main_code, lang)
  nodes : List[pds.PirelNode] = []
  __rec_pre_order(tree.get_root_node(), lang)

  # hacky: remove function definitions as we have rules to translate their headers
  nodes = [n.get_id() if return_node_ids else n
           for n in nodes if n.get_ts_node_type() != 'function_definition']
  return nodes


def _init_tsps(
  template_dict: dict
) -> List[Tuple[str, str]]:
  '''
  Generate TSPs using a new algorithm.
  '''
  tsps = p_generator.generate_tsps_with_generator(template_dict)
  if len(tsps) == 0:
    raise NoTSPsGeneratedError('Could not generate any TSPs')
  p_utils.log_json_time(f'TSPs-generated.json', tsps)
  return tsps


def _get_partial_program(
  subject: p_subject.PirelSubject,
  current_ruleset_str: str,
  template_dict: dict
) -> str:
  '''
  A partial program (TODO is it a good name?) is a partially translated
  program in target language. Partial programs are used in LLM prompts
  to show the context of the code to be translated in the target program.

  IDEA
  Since translation is done in pre-order traversal, the sequence of nodes
  to be translated is:
  1. Nodes for which we have a translation rule
  2. Problematic node, for which we are attempting to learn a translation rule
  3. Nodes that are not translated yet.
  The algorithm is:
  a. Create a hacky rule for problematic node, that translates it into an
     identifier with a special name. This identifier will be the location
     of the translation. Everything around it will be the context.
  b. For each node in (3) create a hacky rule as in (a) with a different
     identifier with a special name, then just remove it from the code later.
     This way we get a partially translated program.
  '''

  def _append_hacky_rules(
    current_ruleset_str: str,
    problematic_node_type: str,
    secret_identifier: str
  ) -> str:
    '''
    Update `trans_rules` by appending all possible hacky rules
    to get a partial program.

    TODO HACKY this function is language dependent
    '''

    # contains possible ways to translate a node in the source language
    # into a node in the target language.
    HACKY_EXPANSIONS_PY_JS = {
      'pair': [
        # replacement for `pair` in `object`
        f'("js.shorthand_property_identifier" (val "{secret_identifier}"))',
      ],
      'default': [
        # convert a node into an identifier directly
        f'("js.identifier" (val "{secret_identifier}"))',

        # convert a node into an identifier under expression statement node
        f'("js.expression_statement" ("js.identifier" (val "{secret_identifier}")))',

        # ignore a node (do not translate)
        f''
      ]
    }

    matcher = f'"py.{problematic_node_type}" "*"'
    for hacky_expansion in HACKY_EXPANSIONS_PY_JS.get(problematic_node_type, HACKY_EXPANSIONS_PY_JS['default']):
      hacky_rule = f'(match_expand (fragment ({matcher}) "*") (fragment {hacky_expansion} "*2"))'
      current_ruleset_str = current_ruleset_str + f'\n\n{hacky_rule}'
    return current_ruleset_str

  def _post_process_partial_program_remove_excess_replace_vars(partial_program: str) -> str:
    '''
    Problem: if a problematic node appears multiple times consecutively in the AST,
    what ends up happening is that partial program contains several consecutive
    replace_var's. This is not good for using with LLMs.
    This function solves this problem by str.replace() by replacing all occurences of
    replace_var's to dummy_var's except the first one.
    The solution is somewhat hacky and not complete, but it's much easier than
    intervening translation process where we require translate() to use different
    rules for the same consecutive node types.
    '''
    li = partial_program.rsplit(
      p_consts.PAR_PROG_PROB_NODE_REPLACE,
      partial_program.count(p_consts.PAR_PROG_PROB_NODE_REPLACE) - 1
    )
    return p_consts.PAR_PROG_DUMMY_IDENTIFIER.join(li)

  # NOTE if the first translation was successful, it means we have all necessary translation rules.
  # If it wasn't successful, then we run a loop in which we introduce `problematic_node -> identifier` rules
  # until we translate the program. This way we generate a partial program.
  logger.debug(f'~~~ Preparing partially translated target code')

  # 1 ADD HACKY RULES FOR THE MAIN PROBLEMATIC NODE
  prob_ntype_main = template_dict['problematic_node_type']
  new_trans_rules = _append_hacky_rules(current_ruleset_str, prob_ntype_main, p_consts.PAR_PROG_PROB_NODE_REPLACE)
  new_src_code = template_dict['template_origin']

  logger.debug(
    f'problematic_node_type_main = "{prob_ntype_main}"\n'
    f'Appended hacky rules for the main problematic node to the ruleset\n'
    f'new_src_code = \n{new_src_code}')

  templates_dict = None
  try:
    duoglot_result_dict = duoglot_translate_wrapper(
      new_src_code,
      subject.src_lang,
      subject.tar_lang,
      new_trans_rules,
      subject.auto_backward,
      subject.choices,
      skip_template_extraction=True
    )
    logger.debug(f'SUCCESS Partial program generation is complete. num_loops=0')
    tar_code = duoglot_result_dict['tar_code']
    partial_program = _post_process_partial_program_remove_excess_replace_vars(tar_code)
    return partial_program
  except d_grammar_expand.TranslationRuleNotFoundException as exc:
    templates_dict = exc.get_templates_dict()

  # 2 ADD HACKY RULES FOR THE SUBSEQUENT PROBLEMATIC NODES
  logger.debug(f'Translation is not over yet: there are still nodes to translate in a hacky way')
  loop_counter = 1

  while True:
    logger.debug(f'Entering partial program generation loop #{loop_counter}')
    assert templates_dict is not None, 'should not happen: templates_dict is None'
    prob_ntype_remaining = templates_dict['problematic_node_type']
    new_trans_rules = _append_hacky_rules(new_trans_rules, prob_ntype_remaining, p_consts.PAR_PROG_DUMMY_IDENTIFIER)

    logger.debug(
      f'prob_ntype_remaining = "{prob_ntype_remaining}". '
      f'Appended hacky rules to the ruleset')

    templates_dict = None
    try:
      duoglot_result_dict = duoglot_translate_wrapper(
        new_src_code,
        subject.src_lang,
        subject.tar_lang,
        new_trans_rules,
        subject.auto_backward,
        subject.choices,
        skip_template_extraction=True
      )
      tar_code = duoglot_result_dict['tar_code']
      partial_program = _post_process_partial_program_remove_excess_replace_vars(tar_code)
      logger.debug(f'SUCCESS Partial program generation is complete. num_loops={loop_counter}')
      logger.debug(f'Partial program is:\n{partial_program}')
      return partial_program
    except d_grammar_expand.TranslationRuleNotFoundException as exc:
      templates_dict = exc.get_templates_dict()

    logger.debug(f'Partial program generation loop #{loop_counter} ended')
    loop_counter += 1


def _artificial_context_if_possible(template_dict: dict) -> Optional[dict]:
  '''
  ["py.module", 0,
    [
      "py.return_statement",
      1,
      "\"return\"", <node>
    ]
  ]
  '''
  logger.debug('Checking if artificial context for expressions can be used')

  context_ntype = template_dict['context_node_type']
  prob_ntype = template_dict['problematic_node_type']
  prob_nid = template_dict['problematic_node_id']
  prob_npath = template_dict['problematic_node_path']
  template_origin = template_dict['template_origin']
  src_lang = template_dict['src_lang']

  if context_ntype == prob_ntype:
    logger.debug(
      f'Artificial context cannot be used: context_node_type == '
      f'problematic_node_type == {context_ntype}')
    return None

  prob_nstr = d_ast_parse.node_id_pretty_print(template_origin, src_lang, prob_nid)
  artif_template_origin = f'return {prob_nstr}'
  artif_prob_npath = [1]

  # check if `artif_template_origin` can be parsed
  if p_utils.does_have_parse_error(artif_template_origin, src_lang):
    logger.debug(
      f'Artificial context cannot be used: could not parse '
      f'artificial template_origin == {artif_template_origin!r}')
    return None

  # check if the problematic node in `artif_template_origin`
  # is the same tree as the original problematic node
  tree1 = pds.DuoGlotTree.from_code_str(template_origin, src_lang)
  tree2 = pds.DuoGlotTree.from_code_str(artif_template_origin, src_lang)
  assert len(tree1.root_node.get_children()) == 1
  assert len(tree2.root_node.get_children()) == 1
  ctx_node1 = tree1.root_node.get_children()[0]
  ctx_node2 = tree2.root_node.get_children()[0]
  prob_node1 = ctx_node1.get_child_by_path(prob_npath)
  prob_node2 = ctx_node2.get_child_by_path(artif_prob_npath)
  assert prob_node1.get_ts_node_type() == prob_ntype == prob_node2.get_ts_node_type(), 'sanity check'
  if not prob_node1.is_similar_to_rec(prob_node2):
    logger.debug(
      f'Artificial context cannot be used: problematic node is parsed '
      f'differently in the artificial template_origin:\n'
      f'template_origin:\n{template_origin}\n'
      f'artificial_template_origin:\n{artif_template_origin}\n')
    return None

  artif_context_ntype = 'return_statement'
  artif_prob_nid = prob_node2.get_id()
  artif_contexts = [
    {
      'source_context': [
        [
          prob_node2.get_type()
        ],
        [
          'py.return_statement'
        ]
      ],
      'target_context': [
        [
          'unknown'
        ],
        [
          'js.return_statement'
        ]
      ]
    }
  ]
  artif_partial_program = f'return {p_consts.PAR_PROG_PROB_NODE_REPLACE};'

  artif_template_dict = {
    'template_id': template_dict['template_id'],
    'src_lang': template_dict['src_lang'],
    'tar_lang': template_dict['tar_lang'],
    'template_origin': artif_template_origin,
    'context_node_type': artif_context_ntype,
    'context_node_id': 1,
    'problematic_node_type': template_dict['problematic_node_type'],
    'problematic_node_id': artif_prob_nid,
    'problematic_node_path': artif_prob_npath,
    'is_valid_template': template_dict['is_valid_template'],
    'is_insert_secret_fn': template_dict['is_insert_secret_fn'],
    'contexts': artif_contexts,
    'partial_program': artif_partial_program,
  }

  return artif_template_dict


def _init_template_dict(
  subject: p_subject.PirelSubject,
  current_ruleset_str: str,
  templates_dict: dict
) -> dict:
  '''
  subject must contain:
  - src_lang
  - tar_lang
  - auto_backward
  - choices
  - get_src_main_code()
  '''

  def _rerun_translation_for_context(
    subject: p_subject.PirelSubject,
    current_ruleset_str: str,
    template_origin: str
  ) -> dict:
    '''
    Why do we need this function?
    We need this function to update certain values in `template_dict`:
    1. context_node_id
    2. problematic_node_id
    3. contexts (mainly)

    NOTE returns a new `template_dict`
    TODO optimize: context extraction is needed only at this step
    RETURN updated `template_dict`
    '''
    try:
      _ = duoglot_translate_wrapper(
        template_origin,
        subject.src_lang,
        subject.tar_lang,
        current_ruleset_str,
        subject.auto_backward,
        subject.choices,
      )
    except d_grammar_expand.TranslationRuleNotFoundException as exc:
      templates_dict = exc.get_templates_dict()
      template_idx = templates_dict['num_templates'] - 1
      return templates_dict[template_idx]
    raise RuntimeError('DuoGlot should have failed to translate the context code')

  logger.debug('Starting template_dict initialization')

  # in cases when templates_dict is loaded from str, keys are strings
  _valid_template_idx = p_utils.to_int(templates_dict['num_templates']) - 1
  template_dict = templates_dict.get(_valid_template_idx) or templates_dict.get(str(_valid_template_idx))

  result = _artificial_context_if_possible(template_dict)
  if result is not None:
    logger.debug(
      'Finished template_dict initialization. Using artificial context.\n'
      f'template_dict:\n{json.dumps(result, indent=2)}')
    p_utils.log_json_time(f'template_dict.json', result)
    return result

  # Rerun DuoGlot translation to obtain `template_dict`
  # for the context code snippet, not the entire program.
  # This is done to get the updated values for
  # `context_node_id`, `problematic_node_id`, and `problematic_node_path`
  template_dict = _rerun_translation_for_context(subject, current_ruleset_str, template_dict['template_origin'])

  # simplify the context
  template_dict = p_grammar.simplify_template(template_dict)

  # simplify the template using the generator
  template_dict = p_generator.simplify_template_with_generator(template_dict)

  # Rerun DuoGlot translation to obtain `template_dict`
  # for the context code snippet, not the entire program.
  # This is done to get the updated values for
  # `context_node_id`, `problematic_node_id`, and `problematic_node_path`
  template_dict = _rerun_translation_for_context(subject, current_ruleset_str, template_dict['template_origin'])

  # prepare partial program
  try:
    partial_program = _get_partial_program(subject, current_ruleset_str, template_dict)
  except Exception as e:
    logger.warning(f'Failed to generate partial program: {e}')
    raise PartialProgramGenerationError(f'Failed to generate partial program: {e}')
  template_dict['partial_program'] = partial_program

  logger.debug(
    'Finished template_dict initialization\n'
    f'template_dict:\n{json.dumps(template_dict, indent=2)}')
  p_utils.log_json_time(f'template_dict.json', template_dict)
  return template_dict


def _combine_prectx_and_simple_ntext(
  pre_context: str,
  snippet_under_test: str
) -> str:

  def __rec_find_special_identifier(node: pvis.AbstractNode) -> Optional[pvpy.IdentifierNode]:
    if isinstance(node, pvpy.IdentifierNode):
      if node.val() == p_consts.PRE_CTX_SPEC_IDENT:
        return node
    for child in node.children:
      res = __rec_find_special_identifier(child)
      if res is not None:
        return res
    return None

  assert pre_context.count(p_consts.PRE_CTX_SPEC_IDENT) == 1, \
    'should not happen: pre_context must contain exactly one line with special identifier'
  pc_tree = pvpy.Tree.from_str(pre_context)
  sut_tree = pvpy.Tree.from_str(snippet_under_test)

  spec_id_node = __rec_find_special_identifier(pc_tree.root_node)
  assert spec_id_node is not None, 'should not happen: could not find special identifier node'
  repl_expr_stat_node = spec_id_node.get_parent()  # will replace expression statement node
  idx_in_parent = repl_expr_stat_node.parent.children.index(repl_expr_stat_node)

  sut_stat_node = sut_tree.root_node
  sut_stat_node.set_parent(repl_expr_stat_node.parent)
  repl_expr_stat_node.parent.children[idx_in_parent] = sut_stat_node

  pp = pvpy.PrettyPrinter(indent_with='    ')
  pp.visit(pc_tree.root_node)
  return '\n'.join(pp.lines)


def _create_subject_for_snippet_learn(
  artif_template_origin: str,
  src_lang: str,
  tar_lang: str,
  subject_name: str,
) -> p_subject.PirelSubject:
  '''
  Create a subject used during snippet-based rule learning
  phase: learn_trans_rules_from_snippet()
  '''

  # all attributes of PirelSubject instance set explicitly
  benchmark_name = 'snippet-learn'
  name = subject_name
  src_program = artif_template_origin
  src_lang = src_lang
  tar_lang = tar_lang
  translation_rules_main_code = None
  translation_rules_test_code = None
  is_three_split = False
  auto_backward = True
  choices = {'type': 'ASTNODE', 'choices_list': []}
  verified_choice_options = []

  # create a subject instance
  snippet_learn_subject = p_subject.PirelSubject(
    benchmark_name, name, src_program, src_lang, tar_lang, is_three_split)
  snippet_learn_subject.translation_rules_main_code = translation_rules_main_code
  snippet_learn_subject.translation_rules_test_code = translation_rules_test_code
  snippet_learn_subject.auto_backward = auto_backward
  snippet_learn_subject.choices = choices
  snippet_learn_subject.verified_choice_options = verified_choice_options

  return snippet_learn_subject


def _create_subject_for_stat_learn(
  main_subject: p_subject.PirelSubject,
  simple_ntext: str,
  current_ruleset: p_ruleset.Ruleset,
  simple_nchoices: dict,
) -> p_subject.PirelSubject:
  '''
  Create a subject used during rule learning phase.
  '''

  # all attributes of PirelSubject instance set explicitly
  benchmark_name = 'stat-learn'
  name = main_subject.name
  src_program = simple_ntext
  src_lang = main_subject.src_lang
  tar_lang = main_subject.tar_lang
  translation_rules_main_code = current_ruleset.to_str_ruleset()
  translation_rules_test_code = None
  is_three_split = False
  auto_backward = True
  choices = simple_nchoices
  verified_choice_options = []

  # create a subject instance
  stat_learn_subject = p_subject.PirelSubject(
    benchmark_name, name, src_program, src_lang, tar_lang, is_three_split)
  stat_learn_subject.translation_rules_main_code = translation_rules_main_code
  stat_learn_subject.translation_rules_test_code = translation_rules_test_code
  stat_learn_subject.auto_backward = auto_backward
  stat_learn_subject.choices = choices
  stat_learn_subject.verified_choice_options = verified_choice_options

  return stat_learn_subject


def _rfind_statement_nid_by_text(
  src_main_code: str,
  statement: str
) -> int:
  '''
  Return the node_id in the AST of src_main_code whose text is statement.
  If there are multiple such nodes, return the rightmost one.
  If there multiple nodes with the same text, return the furthest one
  from the root.
  PRE: statement is not empty and appears in src_main_code.
  '''

  def _rec_rfind(node: pvis.AbstractNode) -> Optional[pvis.AbstractNode]:
    nonlocal statement
    pp = pvpy.PrettyPrinter(indent_with='    ')
    node_text = pp.visit(node)
    node_text = node_text if node_text is not None else '\n'.join(pp.lines)
    if node_text == statement:
      # found matching node, but its child may have the same text
      # e.g. block -> expression_statement
      # need to return the smallest matching node
      all_children_result = [_rec_rfind(child) for child in node.get_nt_children()]
      if all(c is None for c in all_children_result):
        return node
      child_res = [c for c in all_children_result if c is not None]
      assert len(child_res) == 1, 'should not happen: multiple children with the same text'
      return child_res[0]
    for child in reversed(node.get_nt_children()):
      res = _rec_rfind(child)
      if res is not None:
        return res
    return None

  assert statement.strip() != '', 'should not happen: statement is empty'
  assert src_main_code.strip() != '', 'should not happen: src_main_code is empty'

  tree = pvpy.Tree.from_str(src_main_code)
  stat_node = _rec_rfind(tree.root_node)
  assert stat_node is not None, 'should not happen: could not find statement node'

  return stat_node.get_node_id()


def _instrument_with_break_statements(
  src_main_code: str,
  statement: str
) -> str:
  '''
  Insert break statements in loops to avoid infinite loops.
  Break statements are inserted only in loops that are ancestors
  of the statement node or the statement node itself.
  PRE: statement is not empty and appears in src_main_code.
  '''
  stat_nid = _rfind_statement_nid_by_text(src_main_code, statement)
  tree = pvpy.Tree.from_str(src_main_code)
  root_node = tree.root_node

  nid_node_map = root_node.get_nid_node_map()
  assert stat_nid in nid_node_map, 'should not happen: stat_nid not in nid_node_map'
  stat_node = nid_node_map[stat_nid]

  cursor_node = stat_node
  while cursor_node is not None:
    if not isinstance(cursor_node, (pvpy.ForStatementNode, pvpy.WhileStatementNode)):
      cursor_node = cursor_node.get_parent()
      continue
    break_statement = pvpy.BreakStatementNode('break_statement')
    cursor_node.body.children.append(break_statement)
    break_statement.set_parent(cursor_node.body)
    cursor_node = cursor_node.get_parent()

  pp = pvpy.PrettyPrinter(indent_with='    ')
  pp.visit(root_node)
  return '\n'.join(pp.lines)


def _create_src_main_code_for_val(
  src_main_code: str,
  pre_context: str,
  statement: str,
  is_three_split: bool,
) -> str:
  '''
  Return log-instrumented main code for statement node validation.

  This snippet contains the given statement wrapped in its pre-context,
  and if the subject program is in the three-split format,
  wrapped again in the function header if src_main_code.
  '''
  stmt_in_ctx = _combine_prectx_and_simple_ntext(pre_context, statement)
  if is_three_split: # wrap in f_gold
    function_headers = [line for line in src_main_code.splitlines()
                        if line.startswith('def f_gold(')]
    assert len(function_headers) == 1
    fn_header = function_headers[0].strip()
    assert fn_header.endswith('):')
    stmt_in_ctx = f'{fn_header}\n{p_utils.indent(stmt_in_ctx, 4)}'
    stmt_in_ctx = _instrument_with_break_statements(stmt_in_ctx, statement)
    stmt_in_ctx = pvpy.LogStatementInserter.insert_log_statements(stmt_in_ctx)
    stmt_in_ctx = pvpy.LogStatementsIndexer.index_log_statements(stmt_in_ctx)
  else:
    stmt_in_ctx = _instrument_with_break_statements(stmt_in_ctx, statement)
    stmt_in_ctx = pvpy.LogInserterNo3Split.insert_log_statements(stmt_in_ctx)
    stmt_in_ctx = pvpy.LogIndexerNo3Split.index_log_statements(stmt_in_ctx)

  return stmt_in_ctx


def _create_src_program_for_stat_val(
  main_subject: p_subject.PirelSubject,
  pre_context: str,
  simple_ntext: str
) -> str:
  '''
  Test code for statement node validation
  is the same as the main subject's test code.
  '''
  snv_src_test_code = main_subject.get_src_test_code()
  snv_src_main_code = _create_src_main_code_for_val(
    main_subject.get_src_main_code(),
    pre_context,
    simple_ntext,
    main_subject.is_three_split)
  if not main_subject.is_three_split:
    return snv_src_main_code

  '''
  Test call code is a simple hard-coded `test()` string
  '''
  snv_test_call_code = 'test()'

  snv_src_program = p_consts.TEST_SCRIPT_TEMPLATE.format(
    test_code=snv_src_test_code, main_code=snv_src_main_code, test_call_code=snv_test_call_code)
  return snv_src_program


def _create_subject_for_stat_val(
  main_subject: p_subject.PirelSubject,
  pre_context: str,
  simple_ntext: str,
  current_ruleset: p_ruleset.Ruleset,
) -> p_subject.PirelSubject:
  '''
  Create a subject used during validation phase.
  '''
  # all attributes of PirelSubject instance set explicitly
  benchmark_name = 'stat-val'
  name = main_subject.name
  src_program = _create_src_program_for_stat_val(main_subject, pre_context, simple_ntext)
  src_lang = main_subject.src_lang
  tar_lang = main_subject.tar_lang
  translation_rules_main_code = \
    current_ruleset.to_str_ruleset() + '\n\n' + \
    p_utils.read_text(p_consts.LOG_STAT_RULE_FPATH) + '\n\n' + \
    p_utils.read_text(p_consts.RULE_VAL_EXTRA_RULES_FPATH)
  translation_rules_test_code = main_subject.translation_rules_test_code
  is_three_split = main_subject.is_three_split
  auto_backward = True
  choices = {'type': 'ASTNODE', 'choices_list': []}  # default
  verified_choice_options = []  # default, will be set later

  # create a subject instance
  stat_val_subject = p_subject.PirelSubject(
    benchmark_name, name, src_program, src_lang, tar_lang, is_three_split)
  stat_val_subject.translation_rules_main_code = translation_rules_main_code
  stat_val_subject.translation_rules_test_code = translation_rules_test_code
  stat_val_subject.is_three_split = is_three_split
  stat_val_subject.auto_backward = auto_backward
  stat_val_subject.choices = choices
  stat_val_subject.verified_choice_options = verified_choice_options

  return stat_val_subject


def _get_statement_node_text(
  node: pds.PirelNode,
  src_main_code: str,
) -> str:
  '''
  RETURN text of the statement node.
  '''
  tree = pvpy.Tree.from_str(src_main_code)
  root_node = tree.root_node
  nid_node_map = root_node.get_nid_node_map()
  assert node.get_id() in nid_node_map, 'should not happen: node id not in nid_node_map'
  node = nid_node_map[node.get_id()]
  pp = pvpy.PrettyPrinter(indent_with='    ')
  pp.visit(node)
  text = '\n'.join(pp.lines)
  return text


def _simplify_comp_stat_node_text(
  node: pds.PirelNode,
  src_main_code: str,
) -> str:
  '''
  Replaces children of `block` nodes with a pass statement.
  Has no effect on non-compound statement nodes.
  RETURN simplified text of the statement node.
  '''
  text = _get_statement_node_text(node, src_main_code)
  tree = pvpy.Tree.from_str(text)
  sn_simplifier = pvpy.CompStatNodeSimplifier()
  sn_simplifier.visit(tree.root_node)
  pp = pvpy.PrettyPrinter(indent_with='    ')
  simplified_text = pp.visit(tree.root_node)
  return simplified_text


def _get_statement_node_by_id(
  src_main_code: str,
  lang: str,
  node_id: int
) -> pds.PirelNode:
  '''
  Given an id of the statement node, return the node from the source code.
  '''
  tree = pds.PirelTree.from_code_str(src_main_code, lang)
  node = tree.get_root_node().get_node_by_id(node_id)
  return node


def _can_translate(
  src_code: str,
  src_lang: str,
  tar_lang: str,
  translation_rules: str,
  auto_backward: bool,
  choices: dict
) -> Optional[dict]:
  '''
  Check if we can get a translation for the given source code.
  RETURN None if translation is successful, otherwise return templates_dict.
  '''
  try:
    _ = duoglot_translate_wrapper(
      src_code, src_lang, tar_lang, translation_rules, auto_backward, choices)
    return None
  except d_grammar_expand.TranslationRuleNotFoundException as exc:
    templates_dict = exc.get_templates_dict()
    return templates_dict


def duoglot_translate_wrapper(
  src_code: str,
  src_lang: str,
  tar_lang: str,
  trans_rules: str,
  auto_backward: bool = True,
  choices: dict = {'type': 'ASTNODE', 'choices_list': []},
  **kwargs
) -> dict:
  '''
  Wrapper around DuoGlot's `grammar_expand.TransSession.get_translation()`.
  RAISE Propagate all exceptions to the caller.
  RETURN a dict containing all the relevant information about the target program.

  kwargs:
  - skip_template_extraction: bool, optional, default is False
  '''

  p_utils.log_json_time(f'args-duoglot_translate_wrapper.json', locals())

  assert src_code.isascii()
  assert choices['type'] in ['STEP', 'ASTNODE'], 'Unknown choices type'
  slot_dedup_enabled = choices['type'] == 'ASTNODE'

  translator = p_translators.get_translator_cached(
    src_code,
    src_lang,
    tar_lang,
    trans_rules,
    slot_dedup_enabled
  )

  # NOTE raises all sorts of exceptions (check docs)
  # If there are no raised exceptions, it means that the translation was successful.
  tar_ast, dbg_history = translator.get_translation(choices, auto_backward, **kwargs)

  logger.debug(f'SUCCESS DuoGlot translation is successful!')
  tar_code, map_to_exid = d_ast_pretty.ast_to_code(tar_ast, tar_lang)
  return {
    'src_ast': translator.source_ast,
    'src_ann': translator.source_ann,
    'tar_ast': tar_ast,
    'tar_code': tar_code,
    'map_to_exid': map_to_exid,
    'dbg_history': dbg_history,
  }


async def learn_trans_rules_from_snippet(
  snippet: str,
  src_lang: str,
  tar_lang: str,
  ruleset_str: str,
  subject_name: str,
  lrule_learn_snp: Optional[ptlog.RuleLearnSnp] = None
) -> List[str]:
  '''
  Learn translation rules from a code snippet that is an expression.
  PARAM ruleset_str: ruleset that cannot translate the snippet.

  PRE1: artif_template_origin has no parse error
  PRE2: problematic node under artif_context is similar to cursor_prob_node

  NOTE This function is almost identical to learn_trans_rules_for_prob_node
  TODO refactor to reduce code duplication?
  '''
  p_utils.log_json_time(f'args-learn_trans_rules_from_snippet.json', locals())
  assert Config.generator == 'lightweight', 'only lightweight generator is supported here'

  lrule_learn_snp = lrule_learn_snp or ptlog.RuleLearnSnp()
  lrule_learn_snp.snippet = snippet
  lrule_learn_snp.stms = p_utils.current_time_msec()

  # parse as itself
  tree = pds.DuoGlotTree.from_code_str(snippet, src_lang)
  root_node = tree.get_root_node()
  assert len(root_node.get_children()) == 1, 'snippet must contain exactly one context node'
  context_node = root_node.get_children()[0]
  assert context_node.get_ts_node_type() == 'expression_statement', 'context node must be expression_statement'
  prob_node = context_node.get_children()[0]

  # parse under "return {}" artificial context
  artif_template_origin = p_generator_lw.ARTIF_CTX_TEMPLATE.format(snippet)
  # PRE1: check parse error under artificial context
  assert not p_utils.does_have_parse_error(artif_template_origin, src_lang), \
    'PRE1 broken: artificial context template has parse error'
  # PRE2: check similarity of problematic node under artificial context
  artif_tree = pds.DuoGlotTree.from_code_str(artif_template_origin, src_lang)
  assert len(artif_tree.root_node.get_children()) == 1
  artif_ctx_node = artif_tree.root_node.get_children()[0]
  artif_prob_node = artif_ctx_node.get_child_by_path(p_generator_lw.ARTIF_PROB_NPATH)
  assert prob_node.is_similar_to_rec(artif_prob_node), \
    'PRE2 broken: problematic node under artificial context is not similar to cursor_prob_node'

  template_dict = {
    'template_id': 1,
    'template_origin': artif_template_origin,
    'src_lang': src_lang,
    'tar_lang': tar_lang,
    'context_node_type': artif_ctx_node.get_ts_node_type(),
    'context_node_id': artif_ctx_node.get_id(),
    'problematic_node_path': p_generator_lw.ARTIF_PROB_NPATH,
    'is_valid_template': True,
    'is_insert_secret_fn': False,
  }

  # generate TSPs
  tsps, template_dict = p_generator_lw.generate_tsps_lightweight(template_dict)
  if len(tsps) == 0:
    lrule_learn_snp.success = False
    lrule_learn_snp.reason = 'Could not generate any TSPs'
    lrule_learn_snp.etms = p_utils.current_time_msec()
    raise NoTSPsGeneratedError('Could not generate any TSPs')
  p_utils.log_json_time(f'TSPs-generated.json', tsps)

  # create subject for snippet-based learning
  subject = _create_subject_for_snippet_learn(
    artif_template_origin, src_lang, tar_lang, subject_name)

  # iterate over TSPs
  num_useful_tsps = 0
  num_skipped_tsps = 0
  all_trules_list : List[str] = []

  for tsp_idx, tsp in enumerate(tsps, start=1):
    logger.debug(
      f'learn-prob: learning translation rules using TSP ({tsp_idx}/{len(tsps)}):\n'
      f'tsp.id = {tsp_idx}\n{json.dumps(tsp, indent=2)}')

    ltsp = ptlog.TSP()
    ltsp.id = tsp_idx
    ltsp.sp1 = tsp[0]
    ltsp.sp2 = tsp[1]
    lrule_learn_snp.tsps.append(ltsp)

    trules_list = await learn_trans_rules_from_tsp_with_retries(
      tsp, template_dict, subject, ruleset_str, ltsp)
    all_trules_list.extend(trules_list)

    if len(trules_list) == 0:
      logger.warning(
        f'learn-prob: no translation rules were learnt from TSP '
        f'(tsp.id = {tsp_idx}):\n{json.dumps(tsp, indent=2)}')
      num_skipped_tsps += 1
    else:
      num_useful_tsps += 1

    if num_skipped_tsps >= p_consts.MAX_NUM_SKIPPED_TSPS:
      logger.debug('learn-prob: too many skipped TSPs, stopping.')
      break
    if num_useful_tsps >= p_consts.MAX_NUM_USEFUL_TSPS:
      logger.debug('learn-prob: enough useful TSPs, stopping.')
      break

  if len(all_trules_list) > 0:
    lrule_learn_snp.success = True
    lrule_learn_snp.etms = p_utils.current_time_msec()
    logger.debug(f'learn-prob: learned {len(all_trules_list)} translation rules.')
    return all_trules_list

  msg = (
    f'Could not learn any translation rules to translate '
    f'the problematic node with any of the {len(tsps)} TSPs. '
    f'problematic_node_type = "{template_dict["problematic_node_type"]}". '
    f'len(tsps) = {len(tsps)}')
  logger.critical(msg)
  lrule_learn_snp.success = False
  lrule_learn_snp.reason = msg
  lrule_learn_snp.etms = p_utils.current_time_msec()
  raise ProbNode_NoTRule_AllTSPsExhaustedError(msg)


async def learn_trans_rules_from_tsp(
  tsp: Tuple[str, str],
  template_dict: dict,
  subject: p_subject.PirelSubject,
  current_ruleset_str: str,
  ltrule_learn_attempt: Optional[ptlog.TRuleLearnAttempt] = None
) -> List[str]:
  '''
  RETURN All possible valid translation rules inferred from all possible translations of `tsp`.
  RAISE `TSP_NoTRuleLearnedError` if no translation rules were learned from TSP.

  NOTE subject must contain the following attributes:
  - name
  - src_lang
  - tar_lang
  - get_src_main_code()
  - auto_backward
  - choices
  '''

  p_utils.log_json_time(f'args-learn_trans_rules_from_tsp.json', locals())
  logger.debug(
    f'learn-tsp: starting p.pirel.learn_trans_rules_from_tsp:\n'
    f'{json.dumps({"tsp": tsp}, indent=2)}')

  ltrule_learn_attempt = ltrule_learn_attempt or ptlog.TRuleLearnAttempt()
  ltrule_learn_attempt.stms = p_utils.current_time_msec()

  # TRANSLATE TSP TO GET {SP1-TP1, SP2-TP2} (TRANSLATION PAIR)
  lpllm_gen_log = ptlog.PLLMGenLog()
  ltrule_learn_attempt.p_llm_gen_log = lpllm_gen_log
  translation_pairs = await p_llm_gen.get_translation_pairs_from_tsp_less_llm(subject, tsp, template_dict, lpllm_gen_log)
  assert len(translation_pairs) > 0, 'sanity check: translation_pairs must not be empty'

  # INFER TRANSLATION RULES FROM TRANSLATION PAIRS
  lprule_inf_log = ptlog.PRuleInfLog()
  ltrule_learn_attempt.p_rule_inferencer_log = lprule_inf_log
  trules_list = p_rule_inferencer.infer_translation_rules(template_dict, translation_pairs, lprule_inf_log)

  # CHECK TRANSLATION RULES
  lprule_filter_log = ptlog.PRuleFilterLog()
  ltrule_learn_attempt.p_rule_filter_log = lprule_filter_log
  checked_trules_list = p_rule_validator.filter_translation_rules(
    trules_list, subject, current_ruleset_str, lprule_filter_log)

  if len(checked_trules_list) == 0:
    logger.warning('learn-tsp: no translation rules were learned from TSP.')
    ltrule_learn_attempt.success = False
    ltrule_learn_attempt.reason = 'No translation rules were learned from TSP.'
    ltrule_learn_attempt.etms = p_utils.current_time_msec()
    raise TSP_NoTRuleLearnedError('No translation rules were learned from TSP.')

  ltrule_learn_attempt.success = True
  ltrule_learn_attempt.etms = p_utils.current_time_msec()
  logger.debug(f'learn-tsp: learned {len(checked_trules_list)} translation rules from TSP.')
  return checked_trules_list


async def learn_trans_rules_from_tsp_with_retries(
  tsp: Tuple[str, str],
  template_dict: dict,
  subject: p_subject.PirelSubject,
  current_ruleset_str: str,
  ltsp: Optional[ptlog.TSP] = None
) -> List[str]:
  '''
  RETURN All possible translation rules inferred from all possible translations of `tsp`.
  NOTE may return zero translation rules

  subject must contain the following attributes:
  - name
  - src_lang
  - tar_lang
  - get_src_main_code()
  - auto_backward
  - choices
  '''

  ltsp = ltsp or ptlog.TSP()
  ltsp.stms = p_utils.current_time_msec()

  attempt_count = 0
  while attempt_count < p_consts.TSP_NUM_ATTEMPTS:
    attempt_count += 1

    logger.debug(f'learn-tsp: attempting to learn some translation rules from a TSP #{attempt_count}')
    ltrule_learn_attempt = ptlog.TRuleLearnAttempt()
    ltrule_learn_attempt.id = attempt_count
    ltsp.trule_learn_attempts.append(ltrule_learn_attempt)

    try:
      trules_list = await learn_trans_rules_from_tsp(
        tsp, template_dict, subject, current_ruleset_str, ltrule_learn_attempt)
      ltsp.success = True
      ltsp.etms = p_utils.current_time_msec()
      return trules_list

    except p_llm_gen.NoTransPairsFromTSPError as err:
      logger.warning('Attempt to learn translation rules from TSP failed')

    except TSP_NoTRuleLearnedError as err:
      logger.warning('Attempt to learn translation rules from TSP failed')

  msg = f'No trans rules learned from TSP after {p_consts.TSP_NUM_ATTEMPTS} attempts.'
  logger.warning(msg)
  ltsp.success = False
  ltsp.reason = msg
  ltsp.etms = p_utils.current_time_msec()
  return []


async def learn_trans_rules_for_prob_node(
  subject: p_subject.PirelSubject,
  current_ruleset_str: str,
  templates_dict: dict,
  lnode_trans_iter: Optional[ptlog.NodeTransIter] = None
) -> List[str]:
  '''
  Run PiREL translation rule learning module for a problematic node.
  PRE There is a translation error.
  RETURN [translation_rules]
  RAISE `ProbNode_NoTRule_AllTSPsExhaustedError` if couldn't learn a translation rule.
  Our goal is to never raise this error

  NOTE subject must contain the following attributes:
  - name
  - src_lang
  - tar_lang
  - get_src_main_code()
  - auto_backward
  - choices
  '''

  logger.debug(f'learn-prob: starting rule learning for a problematic node.')
  p_utils.log_json_time(f'args-learn_trans_rules_for_prob_node.json', locals())

  lnode_trans_iter = lnode_trans_iter or ptlog.NodeTransIter()
  lnode_trans_iter.stms = p_utils.current_time_msec()

  # ~~~ initialize template_dict and TSPs
  if Config.generator == 'default':
    template_dict = _init_template_dict(subject, current_ruleset_str, templates_dict)
    tsps = _init_tsps(template_dict)
  elif Config.generator == 'lightweight':
    _valid_template_idx = p_utils.to_int(templates_dict['num_templates']) - 1
    template_dict = templates_dict.get(_valid_template_idx) or templates_dict.get(str(_valid_template_idx))
    tsps, template_dict = p_generator_lw.generate_tsps_lightweight(template_dict)
    if len(tsps) == 0:
      lnode_trans_iter.success = False
      lnode_trans_iter.reason = 'Could not generate any TSPs'
      lnode_trans_iter.etms = p_utils.current_time_msec()
      raise NoTSPsGeneratedError('Could not generate any TSPs')
    p_utils.log_json_time(f'TSPs-generated.json', tsps)
  else:
    raise ValueError(f'Unknown generator: {Config.generator}')

  lnode_trans_iter.node_id = template_dict['problematic_node_id']
  lnode_trans_iter.node_type = template_dict['problematic_node_type']
  lnode_trans_iter.template_origin = template_dict['template_origin']

  # ~~~ iterate over TSPs (from abstract to concrete)
  num_useful_tsps = 0
  num_skipped_tsps = 0
  all_trules_list : List[str] = []

  for tsp_idx, tsp in enumerate(tsps, start=1):
    logger.debug(
      f'learn-prob: learning translation rules using TSP ({tsp_idx}/{len(tsps)}):\n'
      f'tsp.id = {tsp_idx}\n{json.dumps(tsp, indent=2)}')

    ltsp = ptlog.TSP()
    ltsp.id = tsp_idx
    ltsp.sp1 = tsp[0]
    ltsp.sp2 = tsp[1]
    lnode_trans_iter.tsps.append(ltsp)

    trules_list = await learn_trans_rules_from_tsp_with_retries(
      tsp, template_dict, subject, current_ruleset_str, ltsp)
    all_trules_list.extend(trules_list)

    if len(trules_list) == 0:
      logger.warning(
        f'learn-prob: no translation rules were learnt from TSP '
        f'(tsp.id = {tsp_idx}):\n{json.dumps(tsp, indent=2)}')
      num_skipped_tsps += 1
    else:
      num_useful_tsps += 1

    if num_skipped_tsps >= p_consts.MAX_NUM_SKIPPED_TSPS:
      logger.debug('learn-prob: too many skipped TSPs, stopping.')
      break
    if num_useful_tsps >= p_consts.MAX_NUM_USEFUL_TSPS:
      logger.debug('learn-prob: enough useful TSPs, stopping.')
      break

  if len(all_trules_list) > 0:
    lnode_trans_iter.success = True
    lnode_trans_iter.etms = p_utils.current_time_msec()
    logger.debug(f'learn-prob: learned {len(all_trules_list)} translation rules.')
    return all_trules_list

  msg = (
    f'Could not learn any translation rules to translate '
    f'the problematic node with any of the {len(tsps)} TSPs. '
    f'problematic_node_type = "{template_dict["problematic_node_type"]}". '
    f'len(tsps) = {len(tsps)}')
  logger.critical(msg)
  lnode_trans_iter.success = False
  lnode_trans_iter.reason = msg
  lnode_trans_iter.etms = p_utils.current_time_msec()
  raise ProbNode_NoTRule_AllTSPsExhaustedError(msg)


async def stat_node_learn_trules_recovery(
  simple_ntext: str,
  src_lang: str,
  tar_lang: str,
  lrule_learn_rec: Optional[ptlog.RuleLearnRec] = None
) -> List[str]:
  '''
  Learn an overfitted rule to translate the statement node as a
  measure to recover from the internal validation failure.
  '''
  p_utils.log_json_time(f'args-stat_node_learn_trules_recovery.json', locals())
  logger.info('Starting statement node translation rule learning (RECOVERY)')
  logger.debug(
    f'--stat-learn-rec--: will learn an overfitted rule '
    f'to translate the statement:\n{simple_ntext}')
  lrule_learn_rec = lrule_learn_rec or ptlog.RuleLearnRec()
  lrule_learn_rec.stms = p_utils.current_time_msec()

  def _synthesize_context(simple_ntext: str, src_lang: str) -> dict:
    tree = pds.DuoGlotTree.from_code_str(simple_ntext, src_lang)
    root_node = tree.get_root_node()
    assert len(root_node.get_children()) == 1, 'root node should have a single child'
    context_node = root_node.get_children()[0]
    return {
      'source_context': [[context_node.get_type()]],
      'target_context': [['unknown']]
    }

  simple_ntext_wsec = pvpy.BlockSecretFunInserter.insert_secret_functions(simple_ntext)
  if simple_ntext != simple_ntext_wsec:
    simple_ntext = simple_ntext_wsec
    logger.debug(f'Inserted secret function invocation:\n{simple_ntext}')

  reference_translations, lget_ref_trans = \
    await p_llm_gen.get_reference_translations(simple_ntext, src_lang, tar_lang)

  lrule_learn_rec.get_ref_trans = lget_ref_trans

  if len(reference_translations) == 0:
    msg = 'No reference translations were generated for the statement node'
    logger.error(msg)
    lrule_learn_rec.success = False
    lrule_learn_rec.reason = msg
    lrule_learn_rec.etms = p_utils.current_time_msec()
    raise CouldNotGenRefTranslationsError(msg)

  context = _synthesize_context(simple_ntext, src_lang)
  overfitted_trules : List[str] = []
  for idx, ref_trans in enumerate(reference_translations, start=1):
    ref_trans = pvjs.CommentsRemover.remove_comments(ref_trans)
    trule = p_rule_inferencer.infer_translation_rule_wrapper(
      translation_pair=[{'source': simple_ntext, 'target': ref_trans}],
      src_lang=src_lang,
      tar_lang=tar_lang,
      context=context,
      is_insert_secret_fn=(p_consts.GENERIC_SECRET_FN in simple_ntext),
      choose_largest_node=True,
      is_ignore_semicolon=False
    )
    logger.debug(
      f'--stat-learn-rec--: Learned translation rule '
      f'{idx}/{len(reference_translations)}:\n{trule}')
    overfitted_trules.append(trule)

  lrule_learn_rec.success = True
  lrule_learn_rec.etms = p_utils.current_time_msec()

  return overfitted_trules


async def stat_node_learn_trules_standard(
  simple_ntext: str,
  simple_nchoices: dict,
  stat_learn_subject: p_subject.PirelSubject,
  current_ruleset: p_ruleset.Ruleset,
  lrule_learn_std: Optional[ptlog.RuleLearnStd] = None
) -> List[str]:
  '''
  A standard way of learning translation rules, where we
  stumble upon a problematic node given some choices,
  and learn translation rule(s) that translate that node.
  The rules returned by this function are validated only
  for syntactic correctness, not for semantic correctness.

  NOTE subject must contain the following attributes:
  - name
  - src_lang
  - tar_lang
  - get_src_main_code()
  - auto_backward
  - choices
  '''

  logger.info('~~ Starting statement node translation rule learning (STANDARD)')
  lrule_learn_std = lrule_learn_std or ptlog.RuleLearnStandard()
  lrule_learn_std.stms = p_utils.current_time_msec()

  _MAX_NUM_ITERS = 50
  new_learned_trules : List[str] = []
  iter_counter = 0

  while iter_counter < _MAX_NUM_ITERS:
    iter_counter += 1
    logger.debug(f'--stat-learn-sta--: rule learn loop (STANDARD) iteration #{iter_counter}')

    lnode_trans_iter = ptlog.NodeTransIter()
    lnode_trans_iter.id = iter_counter
    lrule_learn_std.node_trans_iters.append(lnode_trans_iter)

    templates_dict = _can_translate(
      simple_ntext,
      stat_learn_subject.src_lang,
      stat_learn_subject.tar_lang,
      '\n\n'.join(new_learned_trules) + '\n\n' + current_ruleset.to_str_ruleset(),
      stat_learn_subject.auto_backward,
      simple_nchoices
    )
    if templates_dict is None:
      logger.info('SUCCESS Learned rules to translate statement node (translation successful)')
      logger.debug(f'--stat-learn-sta--: Learned translation rules:\n' + '\n'.join(new_learned_trules))

      lrule_learn_std.success = True
      lrule_learn_std.etms = p_utils.current_time_msec()

      return new_learned_trules

    '''
    At this point we have a problematic node that we cannot translate.
    We need to learn translation rules for this node.
    '''
    trules_list = await learn_trans_rules_for_prob_node(
      stat_learn_subject,
      '\n\n'.join(new_learned_trules) + '\n\n' + current_ruleset.to_str_ruleset(),
      templates_dict,
      lnode_trans_iter
    )

    logger.debug(f'--stat-learn-sta--: appending {len(trules_list)} new translation rules.')
    for trule in trules_list:
      new_learned_trules.append(trule)

  lrule_learn_std.success = False
  lrule_learn_std.reason = f'Hit max iterations: {_MAX_NUM_ITERS}'
  lrule_learn_std.etms = p_utils.current_time_msec()

  raise RuntimeError('stat_node_learn_trules_standard: hit max iterations')


async def stat_node_validate_trules(
  simple_nchoices: dict,
  simple_ntext: str,
  stat_learn_subject: p_subject.PirelSubject,
  stat_val_subject: p_subject.PirelSubject,
  current_ruleset: p_ruleset.Ruleset,
  lstat_node_val: Optional[ptlog.StatNodeVal] = None,
) -> p_ruleset.Ruleset:
  '''
  Return silently if
  1. there are enough rules to translate the statement node
  2. the learned rules pass internal validation

  Raise or propagate exceptions otherwise.
  '''

  p_utils.log_json_time(f'args-stat_node_validate_trules.json', locals())
  logger.info('Starting statement node translation rule validation')
  lstat_node_val = lstat_node_val or ptlog.StatNodeVal()
  lstat_node_val.stms = p_utils.current_time_msec()

  # 1. check for problematic nodes in the statement node
  templates_dict = _can_translate(
    simple_ntext,
    stat_learn_subject.src_lang,
    stat_learn_subject.tar_lang,
    current_ruleset.to_str_ruleset(),
    stat_learn_subject.auto_backward,
    simple_nchoices
  )
  if templates_dict is not None:
    lstat_node_val.v1_enough_rules = False
    if _check_needs_rec_rule_learning_directly(templates_dict):
      raise BypassStaRuleLearningError
    raise _ValidationError_ProblematicNodeExists
  logger.debug('GOOD Statement node has no problematic nodes with current choices.')
  lstat_node_val.v1_enough_rules = True

  # 2. perform internal validation
  '''
  Run test-based rule validation to validate the learned translation rules
  that translate the statement node. This invocation has a call to
  p_rule_applicator.apply_translation_rules() that checks all possible
  translation rule combinations that result in a plausible translation
  of the source test script using the learned translation rules.
  '''
  await p_rule_validator.stat_node_validate_trules_test_based(
    stat_val_subject,
    current_ruleset,
    simple_ntext,
    lstat_node_val,
  )

  lstat_node_val.success = True
  lstat_node_val.etms = p_utils.current_time_msec()
  logger.debug('--stat-val--: finished internal validation successfully')


async def stat_node_main_learn_validate_trules(
  main_subject: p_subject.PirelSubject,
  current_ruleset: p_ruleset.Ruleset,  # starting ruleset + learned rules so far
  stat_nid: int,
  nid_blacklist: list[int],
  lstat_node: Optional[ptlog.StatNode] = None
):
  '''
  Validate current translation rules for the statement node,
  and learn new translation rules based on validation errors.
  NOTE adds new translation rules to the current_ruleset.
  '''
  p_utils.log_json_time(f'args-stat_node_main_learn_validate_trules.json', locals())
  src_main_code = main_subject.get_src_main_code()
  src_lang = main_subject.src_lang

  stat_node = _get_statement_node_by_id(src_main_code, src_lang, stat_nid)
  simple_ntext = _simplify_comp_stat_node_text(stat_node, src_main_code)
  pre_context = get_pre_context(src_main_code, src_lang,
                                main_subject.is_three_split,
                                stat_nid, nid_blacklist)
  simple_nchoices = {'type': 'ASTNODE', 'choices_list': []}
  snippet_learn_counter = {}
  SNIPPET_LEARN_THRESHOLD = 2

  lstat_node = lstat_node or ptlog.StatNode()
  lstat_node.stms = p_utils.current_time_msec()
  lstat_node.node_id = stat_nid
  lstat_node.node_text = _get_statement_node_text(stat_node, src_main_code)
  lstat_node.pre_context = pre_context
  lstat_node.simple_ntext = simple_ntext

  logger.debug(
    f'--stat-main--: statement node (nid={stat_nid}): '
    f'Starting rule learning and validation for statement node:\n{simple_ntext}')
  p_utils.log_file_time(f'pre_context.{src_lang}', pre_context)

  _MAX_NUM_ITERS = 4
  iter_counter = 0
  while iter_counter < _MAX_NUM_ITERS:
    iter_counter += 1
    logger.debug(
      f'--stat-main--: statement node (nid={stat_nid}): '
      f'main validate-learn loop iteration #{iter_counter}')

    lstat_node_val = ptlog.StatNodeVal()
    lstat_node.val_learn_iters.append(lstat_node_val)

    stat_learn_subject = _create_subject_for_stat_learn(
      main_subject, simple_ntext, current_ruleset, simple_nchoices)
    stat_val_subject = _create_subject_for_stat_val(
      main_subject, pre_context, simple_ntext, current_ruleset)

    iter_learned_sta_trules : List[str] = []
    iter_learned_rec_trules : List[str] = []

    try:
      logger.debug(
        f'--stat-main--: statement node (nid={stat_nid}): '
        f'about to start validation of learned rules')
      p_utils.log_file_time(f'learned_rules_so_far.snart', current_ruleset.to_str_ruleset())
      p_utils.log_json_time(f'learned_rules_so_far.json', current_ruleset.to_dict())
      await stat_node_validate_trules(
        simple_nchoices,
        simple_ntext,
        stat_learn_subject,
        stat_val_subject,
        current_ruleset,
        lstat_node_val,
      )
      logger.info(
        f'--stat-main--: statement node (nid={stat_nid}): '
        f'SUCCESS Statement node translation rules validated successfully')
      lstat_node.success = True
      lstat_node.etms = p_utils.current_time_msec()
      return

    except p_rule_validator.RulesExistNoneValid as err:
      logger.warning(
        f'--stat-main--: statement node (nid={stat_nid}): '
        f'RulesExistNoneValid:\n'
        f'Most likely missing a valid rule')

      lstat_node_val.success = False
      lstat_node_val.reason = 'Most likely missing a valid rule'
      lstat_node_val.etms = p_utils.current_time_msec()

      lrule_learn_rec = ptlog.RuleLearnRec()
      lstat_node.val_learn_iters.append(lrule_learn_rec)

      iter_learned_rec_trules = await stat_node_learn_trules_recovery(
        simple_ntext,
        stat_learn_subject.src_lang,
        stat_learn_subject.tar_lang,
        lrule_learn_rec,
      )

    except _ValidationError_ProblematicNodeExists:
      logger.info(
        f'--stat-main--: statement node (nid={stat_nid}): '
        f'_ValidationError_ProblematicNodeExists:\n'
        f'There is a node with no translation rules to handle it. '
        f'Will start the STANDARD rule learning procedure.')

      lstat_node_val.success = False
      lstat_node_val.reason = 'There is a node with no translation rules to handle it.'
      lstat_node_val.etms = p_utils.current_time_msec()

      lrule_learn_std = ptlog.RuleLearnStd()
      lstat_node.val_learn_iters.append(lrule_learn_std)

      try:
        iter_learned_sta_trules = await stat_node_learn_trules_standard(
          simple_ntext,
          simple_nchoices,
          stat_learn_subject,
          current_ruleset,
          lrule_learn_std,
        )

      except NoTSPsGeneratedError as err:
        logger.warning(
          f'--stat-main--: statement node (nid={stat_nid}): '
          f'NoTSPsGeneratedError:\n'
          f'No TSPs (two generated snippets in src lang) were generated. '
          f'Will start the RECOVERY rule learning procedure.')

        lrule_learn_std.success = False
        lrule_learn_std.reason = 'No TSPs were generated.'
        lrule_learn_std.etms = p_utils.current_time_msec()

        lrule_learn_rec = ptlog.RuleLearnRec()
        lstat_node.val_learn_iters.append(lrule_learn_rec)

        iter_learned_rec_trules = await stat_node_learn_trules_recovery(
          simple_ntext,
          stat_learn_subject.src_lang,
          stat_learn_subject.tar_lang,
          lrule_learn_rec,
        )

      except ProbNode_NoTRule_AllTSPsExhaustedError as err:
        logger.warning(
          f'--stat-main--: statement node (nid={stat_nid}): '
          f'ProbNode_NoTRule_AllTSPsExhaustedError:\n'
          f'Could not learn any translation rules to translate the problematic node '
          f'with any of the TSPs. Will start the RECOVERY rule learning procedure.')

        lrule_learn_std.success = False
        lrule_learn_std.reason = 'All TSPs used but no translation rules were learned.'
        lrule_learn_std.etms = p_utils.current_time_msec()

        lrule_learn_rec = ptlog.RuleLearnRec()
        lstat_node.val_learn_iters.append(lrule_learn_rec)

        iter_learned_rec_trules = await stat_node_learn_trules_recovery(
          simple_ntext,
          stat_learn_subject.src_lang,
          stat_learn_subject.tar_lang,
          lrule_learn_rec,
        )

      except PartialProgramGenerationError as err:
        logger.warning(
          f'--stat-main--: statement node (nid={stat_nid}): '
          f'PartialProgramGenerationError:\n'
          f'Could not generate a partial program for the statement node. '
          f'Will start the RECOVERY rule learning procedure.')

        lrule_learn_std.success = False
        lrule_learn_std.reason = 'Could not generate a partial program for a node.'
        lrule_learn_std.etms = p_utils.current_time_msec()

        lrule_learn_rec = ptlog.RuleLearnRec()
        lstat_node.val_learn_iters.append(lrule_learn_rec)

        iter_learned_rec_trules = await stat_node_learn_trules_recovery(
          simple_ntext,
          stat_learn_subject.src_lang,
          stat_learn_subject.tar_lang,
          lrule_learn_rec,
        )

    except p_ext_rule_chooser.RuleCombinationsExhaustedError as err:
      logger.warning(
        f'--stat-main--: statement node (nid={stat_nid}): '
        f'p_ext_rule_chooser.RuleCombinationsExhaustedError:\n'
        f'No combination of rules leads to a plausible translation. '
        f'Will start the RECOVERY rule learning procedure.')

      lstat_node_val.success = False
      lstat_node_val.reason = 'No combination of rules leads to a plausible translation.'
      lstat_node_val.etms = p_utils.current_time_msec()

      lrule_learn_rec = ptlog.RuleLearnRec()
      lstat_node.val_learn_iters.append(lrule_learn_rec)

      iter_learned_rec_trules = await stat_node_learn_trules_recovery(
        simple_ntext,
        stat_learn_subject.src_lang,
        stat_learn_subject.tar_lang,
        lrule_learn_rec,
      )

    except p_ext_rule_chooser.QueueInfiniteLoopError as err:
      logger.warning(
        f'--stat-main--: statement node (nid={stat_nid}): '
        f'p_ext_rule_chooser.QueueInfiniteLoopError:\n'
        f'Cannot obtain a plausible translation of a choicable expression '
        f'due to an infinite loop in the matcher queue. '
        f'Will start the RECOVERY rule learning procedure.')

      lstat_node_val.success = False
      lstat_node_val.reason = 'Infinite loop in the matcher queue.'
      lstat_node_val.etms = p_utils.current_time_msec()

      lrule_learn_rec = ptlog.RuleLearnRec()
      lstat_node.val_learn_iters.append(lrule_learn_rec)

      iter_learned_rec_trules = await stat_node_learn_trules_recovery(
        simple_ntext,
        stat_learn_subject.src_lang,
        stat_learn_subject.tar_lang,
        lrule_learn_rec,
      )

    except p_ext_rule_chooser.AllRulesInMatcherGroupImplausibleError as err:
      logger.warning(
        f'--stat-main--: statement node (nid={stat_nid}): '
        f'p_ext_rule_chooser.AllRulesInMatcherGroupImplausibleError:\n'
        f'No rule to plausibly translate a sub-expression. '
        f'Will learn an additional rule by the STANDARD procedure.')

      lstat_node_val.success = False
      lstat_node_val.reason = 'No rule to plausibly translate a sub-expression.'
      lstat_node_val.etms = p_utils.current_time_msec()

      lrule_learn_snp = ptlog.RuleLearnSnp()
      lstat_node.val_learn_iters.append(lrule_learn_snp)

      snippet = err.snippet
      snippet_learn_counter[snippet] = snippet_learn_counter.get(snippet, 0) + 1

      if snippet_learn_counter[snippet] <= SNIPPET_LEARN_THRESHOLD:

        try:
          iter_learned_sta_trules = await learn_trans_rules_from_snippet(
            snippet,
            stat_learn_subject.src_lang,
            stat_learn_subject.tar_lang,
            err.not_matching_rules_str,
            stat_learn_subject.name,
            lrule_learn_snp,
          )

        except ProbNode_NoTRule_AllTSPsExhaustedError as err:
          logger.warning(
            f'--stat-main--: statement node (nid={stat_nid}): '
            f'ProbNode_NoTRule_AllTSPsExhaustedError from learn_trans_rules_from_snippet():\n'
            f'Could not learn any translation rules to translate the problematic node '
            f'with any of the TSPs. Will start the RECOVERY rule learning procedure.')

          lrule_learn_snp.success = False
          lrule_learn_snp.reason = 'All TSPs used but no translation rules were learned.'
          lrule_learn_snp.etms = p_utils.current_time_sec()

          lrule_learn_rec = ptlog.RuleLearnRec()
          lstat_node.val_learn_iters.append(lrule_learn_rec)

          iter_learned_rec_trules = await stat_node_learn_trules_recovery(
            simple_ntext,
            stat_learn_subject.src_lang,
            stat_learn_subject.tar_lang,
            lrule_learn_rec,
          )

      else:
        logger.warning(
          f'--stat-main--: statement node (nid={stat_nid}): '
          f'snippet rule learning hit threshold ({SNIPPET_LEARN_THRESHOLD}), '
          f'will start RECOVERY procedure instead:\n{snippet}')

        lrule_learn_rec = ptlog.RuleLearnRec()
        lstat_node.val_learn_iters.append(lrule_learn_rec)

        iter_learned_rec_trules = await stat_node_learn_trules_recovery(
          simple_ntext,
          stat_learn_subject.src_lang,
          stat_learn_subject.tar_lang,
          lrule_learn_rec,
        )

    except p_ext_rule_chooser.VerifiedRulesExhaustedError as err:
      logger.warning(
        f'--stat-main--: statement node (nid={stat_nid}): '
        f'p_ext_rule_chooser.VerifiedRulesExhaustedError:\n'
        'All verified rules were exhausted and no plausible translation found. '
        'Will learn an additional rule by the STANDARD procedure.')

      lstat_node_val.success = False
      lstat_node_val.reason = 'All verified rules were exhausted and no plausible translation found.'
      lstat_node_val.etms = p_utils.current_time_sec()

      lrule_learn_snp = ptlog.RuleLearnSnp()
      lstat_node.val_learn_iters.append(lrule_learn_snp)

      snippet = err.no_choices_snippet
      snippet_learn_counter[snippet] = snippet_learn_counter.get(snippet, 0) + 1

      if snippet_learn_counter[snippet] <= SNIPPET_LEARN_THRESHOLD:
        iter_learned_sta_trules = await learn_trans_rules_from_snippet(
          snippet,
          stat_learn_subject.src_lang,
          stat_learn_subject.tar_lang,
          err.not_matching_rules_str,
          stat_learn_subject.name,
          lrule_learn_snp,
        )
      else:
        logger.warning(
          f'--stat-main--: statement node (nid={stat_nid}): '
          f'snippet rule learning hit threshold ({SNIPPET_LEARN_THRESHOLD}), '
          f'will start RECOVERY procedure instead:\n{snippet}')

        raise NotImplementedError('recovery rule should be learned for parent statement node')

        lrule_learn_rec = ptlog.RuleLearnRec()
        lstat_node.val_learn_iters.append(lrule_learn_rec)

        iter_learned_rec_trules = await stat_node_learn_trules_recovery(
          simple_ntext,
          stat_learn_subject.src_lang,
          stat_learn_subject.tar_lang,
          lrule_learn_rec,
        )

    except prapp.SrcTestScriptProblematicNodeError as err:
      logger.warning(
        f'--stat-main--: statement node (nid={stat_nid}): '
        f'prapp.SrcTestScriptProblematicNodeError:\n'
        f'The source test script has a problematic node. '
        f'Will start the RECOVERY rule learning procedure.')

      lstat_node_val.success = False
      lstat_node_val.reason = 'The source test script has a problematic node.'
      lstat_node_val.etms = p_utils.current_time_msec()

      lrule_learn_rec = ptlog.RuleLearnRec()
      lstat_node.val_learn_iters.append(lrule_learn_rec)

      iter_learned_rec_trules = await stat_node_learn_trules_recovery(
        simple_ntext,
        stat_learn_subject.src_lang,
        stat_learn_subject.tar_lang,
        lrule_learn_rec,
      )

    except BypassStaRuleLearningError as err:
      logger.info(
        f'--stat-main--: statement node (nid={stat_nid}): '
        f'BypassStaRuleLearningError:\n'
        f'Directly learning a recovery rule for statement:\n{simple_ntext}')

      lstat_node_val.success = False
      lstat_node_val.reason = 'Directly learning a recovery rule (bypass standard rule learning).'
      lstat_node_val.etms = p_utils.current_time_msec()

      lrule_learn_rec = ptlog.RuleLearnRec()
      lstat_node.val_learn_iters.append(lrule_learn_rec)

      iter_learned_rec_trules = await stat_node_learn_trules_recovery(
        simple_ntext,
        stat_learn_subject.src_lang,
        stat_learn_subject.tar_lang,
        lrule_learn_rec,
      )

    # ADD LEARNED RULES TO THE CURRENT RULESET
    if len(iter_learned_sta_trules) > 0:
      logger.debug(
        f'--stat-main--: statement node (nid={stat_nid}): '
        f'simple_ntext:\n{simple_ntext}\n'
        f'learned {len(iter_learned_sta_trules)} new translation rules by STANDARD procedure:\n'
        f'{"\n".join(iter_learned_sta_trules)}\n'
        f'Adding learned standard translation rules to the current ruleset')
      for rule_str in reversed(iter_learned_sta_trules):
        rule_parsed = p_ruleset.TRuleBase.parse_rule_str(rule_str)
        rule = p_ruleset.StandardTRule(rule_parsed, stat_nid, simple_ntext)
        if current_ruleset.get_rule_ref(rule) is not None:
          logger.debug(f'skipping duplicate rule:\n{rule}')
          continue
        current_ruleset.prepend_rule(rule)
    elif len(iter_learned_rec_trules) > 0:
      logger.debug(
        f'--stat-main--: statement node (nid={stat_nid}): '
        f'simple_ntext:\n{simple_ntext}\n'
        f'learned {len(iter_learned_rec_trules)} new translation rules by RECOVERY procedure:\n'
        f'{"\n".join(iter_learned_rec_trules)}\n'
        f'Adding learned overfitted translation rules to the current ruleset')
      for rule_str in reversed(iter_learned_rec_trules):
        rule_parsed = p_ruleset.TRuleBase.parse_rule_str(rule_str)
        rule = p_ruleset.StatementOverfittedTRule(rule_parsed, stat_nid, simple_ntext)
        if current_ruleset.get_rule_ref(rule) is not None:
          logger.debug(f'skipping duplicate rule:\n{rule}')
          continue
        current_ruleset.prepend_rule(rule)
    else:
      lstat_node.success = False
      lstat_node.reason = 'should not happen: no learned translation rules'
      lstat_node.etms = p_utils.current_time_msec()
      raise RuntimeError('should not happen: no learned translation rules')

  lstat_node.success = False
  lstat_node.reason = f'hit max iterations ({_MAX_NUM_ITERS})'
  lstat_node.etms = p_utils.current_time_msec()
  raise RuntimeError('stat_node_main_learn_validate_trules: hit max iterations')


async def learn_trans_rules_for_subject(
  subject: p_subject.PirelSubject,
  starting_ruleset: p_ruleset.Ruleset,
  lrule_learn_phase: Optional[ptlog.RuleLearnPhase] = None
):
  '''
  Iterate over statement nodes in the source code of the subject,
  learn translation rules for each statement node,
  validate the learned rules, and if necessary recover from errors.
  NOTE writes learned translation rules to starting_ruleset.
  NOTE All errors propagate to the caller.
  '''

  '''
  Iterate over statement nodes (simple statements, compound statements).
  It happens that the statement nodes are also context nodes for any problematic node.
  Using this relation between context nodes and statement nodes,
  we will make a list of such nodes.
  '''
  stat_nodes = await _get_statement_nodes(
    subject.get_src_main_code(), subject.src_lang, subject.is_three_split)
  logger.info(
    f'There are {len(stat_nodes)} statement nodes in src_main_code:\n'
    f'{subject.get_src_main_code()}')

  lrule_learn_phase = lrule_learn_phase or ptlog.RuleLearnPhase()
  lrule_learn_phase.stms = p_utils.current_time_msec()
  lrule_learn_phase.num_stat_nodes = len(stat_nodes)

  for sn_idx, stat_node in enumerate(stat_nodes, start=1):
    logger.info(f'---stat-main---: statement node {sn_idx}/{len(stat_nodes)}')
    lstat_node = ptlog.StatNode()
    lstat_node.id = sn_idx
    lrule_learn_phase.stat_nodes.append(lstat_node)

    # writes new rules to starting_ruleset
    await stat_node_main_learn_validate_trules(
      subject,
      starting_ruleset,
      stat_node.get_id(),
      [node.get_id() for node in stat_nodes[sn_idx:]],
      lstat_node
    )

    # NOTE can be used to resume learning from a specific statement node
    logger.debug(f'Saving intermediate ruleset after statement node {sn_idx}/{len(stat_nodes)}')
    p_utils.log_json_time(f'intermediate_ruleset_after_stat_node_{sn_idx}.json',
                          starting_ruleset.to_dict())

  logger.debug(f'Finished learning translation rules for all {len(stat_nodes)} statement nodes')


# TEST HARNESSES
def _test_stat_node_validate_trules():
  '''
  async def stat_node_validate_trules(
    simple_nchoices: dict,
    simple_ntext: str,
    stat_learn_subject: p_subject.PirelSubject,
    stat_val_subject: p_subject.PirelSubject,
    current_ruleset: p_ruleset.Ruleset,
    lstat_node_val: Optional[ptlog.StatNodeVal] = None,
  ) -> p_ruleset.Ruleset:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_stat_node_validate_trules_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  simple_nchoices = args_dict['simple_nchoices']
  simple_ntext = args_dict['simple_ntext']
  stat_learn_subject = p_subject.PirelSubject.from_dict(args_dict['stat_learn_subject'])
  stat_val_subject = p_subject.PirelSubject.from_dict(args_dict['stat_val_subject'])
  current_ruleset = p_ruleset.Ruleset.from_dict(args_dict['current_ruleset'])

  ruleset = asyncio.run(stat_node_validate_trules(
    simple_nchoices,
    simple_ntext,
    stat_learn_subject,
    stat_val_subject,
    current_ruleset
  ))

  print(ruleset.to_str_ruleset())


def _test_stat_node_main_learn_validate_trules():
  '''
  async def stat_node_main_learn_validate_trules(
    main_subject: p_subject.PirelSubject,
    current_ruleset: p_ruleset.Ruleset,  # starting ruleset + learned rules so far
    stat_nid: int,
    nid_blacklist: list[int],
    lstat_node: Optional[ptlog.StatNode] = None
  ):
  '''
  config_fpath = p_consts.TMP_DIR / 'test_stat_node_main_learn_validate_trules_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  main_subject = p_subject.PirelSubject.from_dict(args_dict['main_subject'])
  current_ruleset = p_ruleset.Ruleset.from_dict(args_dict['current_ruleset'])
  stat_nid = args_dict['stat_nid']
  nid_blacklist = args_dict['nid_blacklist']

  asyncio.run(stat_node_main_learn_validate_trules(
    main_subject,
    current_ruleset,
    stat_nid,
    nid_blacklist,
  ))


def _test_learn_trans_rules_for_prob_node():
  '''
  async def learn_trans_rules_for_prob_node(
    subject: p_subject.PirelSubject,
    current_ruleset_str: str,
    templates_dict: dict,
    lnode_trans_iter: Optional[ptlog.NodeTransIter] = None
  ) -> List[str]:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_learn_trans_rules_for_prob_node_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  subject = p_subject.PirelSubject.from_dict(args_dict['subject'])
  current_ruleset_str = args_dict['current_ruleset_str']
  templates_dict = args_dict['templates_dict']

  result = asyncio.run(learn_trans_rules_for_prob_node(
    subject,
    current_ruleset_str,
    templates_dict
  ))
  print('\n\n'.join(result))


def _test_stat_node_learn_trules_recovery():
  '''
  async def stat_node_learn_trules_recovery(
    simple_ntext: str,
    src_lang: str,
    tar_lang: str,
  ) -> List[str]:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_stat_node_learn_trules_recovery_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  simple_ntext = args_dict['simple_ntext']
  src_lang = args_dict['src_lang']
  tar_lang = args_dict['tar_lang']

  result = asyncio.run(stat_node_learn_trules_recovery(simple_ntext, src_lang, tar_lang))
  print('\n\n'.join(result))


def _test_duoglot_translate_wrapper():
  '''
  def duoglot_translate_wrapper(
    src_code: str,
    src_lang: str,
    tar_lang: str,
    trans_rules: str,
    auto_backward: bool,
    choices: dict,
    **kwargs
  ) -> dict:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_duoglot_translate_wrapper_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  src_code = args_dict['src_code']
  src_lang = args_dict['src_lang']
  tar_lang = args_dict['tar_lang']
  trans_rules = args_dict['trans_rules']
  auto_backward = args_dict['auto_backward']
  choices = args_dict['choices']
  kwargs = args_dict['kwargs']

  try:
    result = duoglot_translate_wrapper(
      src_code,
      src_lang,
      tar_lang,
      trans_rules,
      auto_backward,
      choices,
      **kwargs
    )
    # print(json.dumps(result, indent=2))
    print(result['tar_code'])
  except d_grammar_expand.TranslationRuleNotFoundException as exc:
    templates_dict = exc.get_templates_dict()
    print(f'Error: {exc}')
    print(f'Templates dict:\n{json.dumps(templates_dict, indent=2)}')
  except Exception as exc:
    p_utils.write_tmp_json('dbg_history.json', exc.dbg_history)
    print(f'{type(exc).__name__}: {exc}')


def _test_duoglot_translate_wrapper_quick():
  src_code = p_utils.read_tmp_text('src.py')
  translation_rules = p_utils.read_tmp_text('src.snart')
  src_lang, tar_lang = 'py', 'js'
  auto_backward = True
  choices = {'type': 'ASTNODE', 'choices_list': []}
  result = duoglot_translate_wrapper(
    src_code,
    src_lang,
    tar_lang,
    translation_rules,
    auto_backward,
    choices
  )
  print(result['tar_code'])


def _test_get_pre_context():
  '''
  def _get_pre_context(
    src_main_code: str,
    lang: str,
    stat_nid: int
  ) -> str:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_get_pre_context_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  src_main_code = args_dict['src_main_code']
  lang = args_dict['lang']
  stat_nid = args_dict['stat_nid']

  pre_context = get_pre_context(src_main_code, lang, stat_nid)
  print(src_main_code)
  print(f'Pre-context for statement node {stat_nid}:\n{pre_context}')


def _test_learn_trans_rules_from_snippet():
  '''
  async def learn_trans_rules_from_snippet(
    snippet: str,
    src_lang: str,
    tar_lang: str,
    ruleset_str: str,
    subject_name: str,
    lnode_trans_iter: Optional[ptlog.NodeTransIter] = None
  ) -> List[str]:
  '''
  config_fpath = p_consts.TMP_DIR / 'test_learn_trans_rules_from_snippet_config.yaml'
  config = p_utils.read_yaml(config_fpath)
  args_dict = p_utils.read_json(config['args_dict_fpath'])

  snippet = args_dict['snippet']
  src_lang = args_dict['src_lang']
  tar_lang = args_dict['tar_lang']
  ruleset_str = args_dict['ruleset_str']
  subject_name = args_dict['subject_name']

  result = asyncio.run(learn_trans_rules_from_snippet(
    snippet,
    src_lang,
    tar_lang,
    ruleset_str,
    subject_name
  ))
  print('\n\n'.join(result))


if __name__ == '__main__':
  # _test_stat_node_validate_trules()
  # _test_stat_node_main_learn_validate_trules()
  # _test_learn_trans_rules_for_prob_node()
  # _test_stat_node_learn_trules_recovery()
  _test_duoglot_translate_wrapper()
  # _test_duoglot_translate_wrapper_quick()
  # _test_get_pre_context()
  # _test_learn_trans_rules_from_snippet()
