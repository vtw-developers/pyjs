import copy
from typing import List, Tuple, Union

import d_ast_parse
import p_data_structures as pds
import p_utils


logger = p_utils.setup_logger(__name__)


class _CptrError(RuntimeError):
  '''Error type used internally'''


class TemplateTree(pds.PirelTree):
  '''
  Features:
  1. It is formed only from the full AST
  2. It accepts a problematic node id and marks the respective
     node in the Tree as problematic. This is accomplished based
     on the fact that sub-AST is a child of full AST and has the
     same node_id's for the corresponding nodes.
  3. It allows configurable templatization. That is, any node can
     be templatized.
  4. It allows Tree reduction/simplification:
     To make more compact templates (e.g. with function bodies of
     arbitrary size to be replaced with smaller statements)
  '''

  def __init__(
    self,
    full_ast_text: list,
    annotation: dict,
    problematic_node_id: int,
  ) -> None:
    '''
    full_ast_text: Pirel-style AST of the full program
    problematic_node_id: id of problematic node

    full_ast_text:
    Complete AST with pretty-print ready text.
      grammar:
      Node: [type_text, id, Node+] || str
      type_text: [type, text]
      id: int
    '''

    super().__init__(full_ast_text, annotation=annotation)

    assert isinstance(full_ast_text, list)
    assert isinstance(problematic_node_id, int)

    problematic_node_ref = self.get_node_with_id(problematic_node_id)
    assert problematic_node_ref is not None, 'cannot find a problematic node with given problematic AST'
    self.problematic_node = problematic_node_ref

  def get_problematic_node(self) -> 'pds.PirelNode':
    return self.problematic_node

  def get_copy_with_fixed_indentation(self):
    '''
    return a copy instead of mutating self
    NOTE self.full_ast_text is available from superclass
    '''
    tree = TemplateTree(
      self.full_ast_text,
      self.annotation,
      self.problematic_node.get_id()
    )
    tree._fix_indentation()
    return tree

  def debug_print(self):
    def visit_fn(node: pds.PirelNode):
      print('~~~ node_type =', node.get_type())
      print('~~~ node_id =', node.get_id())
      print('~~~ node_text:')
      print(node.get_text())
      print()
    def visit_fn_2(node: pds.PirelNode):
      print(node)
      print()
    self._pre_order(self.root_node, visit_fn_2)
    print('~~~ root_node:', self.get_root_node())
    print('~~~ problematic_node:', self.get_problematic_node())

  def get_template_dict_for_node_id(self, template_node_id: int, context_node_id: int, lang: str) -> dict:
    '''
    Given a context_node_id, template_node_id,
    return a template rooted at context_node_id with template_node_id templatized

    PRE1: template_node_id is sub-node of context_node_id

    PARAMS
    context_node_id - id of node within self, root node of context
    template_node_id - id of node within self, root of templatized nodes

    INTERNAL
    template_node - node at template_node_id, root node of all nodes that will be templatized
    context_node - node at context_node_id, root node of context
    '''

    tree_fixed_indentation = self.get_copy_with_fixed_indentation()

    template_node = tree_fixed_indentation.get_node_with_id(template_node_id)
    context_node = tree_fixed_indentation.get_node_with_id(context_node_id)

    # sanity check
    assert template_node is not None, f'Node (template) with node_id={template_node_id} is not found.'
    assert context_node is not None, f'Node (context) with node_id={template_node_id} is not found.'
    assert context_node.is_ancestor_or_itself(template_node), 'The node to be templatized should be descendant of context node or itself'

    def _count_leading_spaces(text: str) -> int:
        return len(text) - len(text.lstrip(' '))

    def _remove_leading_spaces(text: str) -> str:
      '''remove equal number of leading spaces from all lines in `text` until possible'''
      lines = text.split('\n')
      num_spaces_to_remove = min([_count_leading_spaces(line) for line in lines])
      return '\n'.join([line[num_spaces_to_remove:] for line in lines])

    # 1 extract template node as if it is a program on its own
    def _get_updated_template_context_nodes(template_node: pds.PirelNode, context_node: pds.PirelNode):
      ''''''
      # 1 find the path to template_node from parent_node
      rel_path = context_node.get_path_to_child(template_node)
      # 2 get the template text
      context_text = context_node.get_text()
      context_text = _remove_leading_spaces(context_text)
      # 3 parse the text as it is
      context_ast_text, context_annotation = d_ast_parse.parse_text_dbg(context_text, lang=lang, keep_text=True)
      context_tree = pds.PirelTree(context_ast_text, annotation=context_annotation)
      context_tree._fix_indentation()
      # 4 get updated template_node and parent_node
      # NOTE root node is always top level node (moduly in python)
      # the template_node, however, is its only child (related to rule inference)
      new_context_node = context_tree.get_root_node().get_children()[0]
      new_template_node = new_context_node.get_child_by_path(rel_path)
      return context_tree, new_template_node, new_context_node
    tree_fixed_indentation, template_node, context_node = _get_updated_template_context_nodes(template_node, context_node)

    return_data = {}
    return_data['template_origin'] = context_node.get_text()
    return_data['problematic_node_path'] = context_node.get_path_to_child(template_node)
    return return_data


def extract_templates(
  problematic_ast: list,
  full_ast: list,
  full_ast_text: list,
  ast_annotation: dict,
  src_lang: str,
  tar_lang: str,
  contexts: List[dict],
  **kwargs
) -> dict:
  '''
  IDEAS
  - Grow the context starting from the problematic node up until the root node
  - Generate 'shallow' templates
  '''

  subject_name = kwargs['subject_name']
  # p_utils.log_json_time(f'{subject_name}_problematic_ast.json', problematic_ast)
  # p_utils.log_json_time(f'{subject_name}_full_ast_text.json', full_ast_text)
  # p_utils.log_json_time(f'{subject_name}_full_ast.json', full_ast)

  # 1 instantiate a `TemplateTree` - data structure for creating templates
  problematic_node_id = problematic_ast[1]
  template_tree = TemplateTree(full_ast_text, ast_annotation, problematic_node_id)
  problematic_node = template_tree.get_problematic_node()

  # 2 instantiate `templates_dict`
  # `templates_dict` contains templates for all valid contexts
  templates_dict = {}
  templates_dict['problematic_node_type'] = problematic_node.get_ts_node_type()
  templates_dict['problematic_node_id'] = problematic_node.get_id()

  # 3 loop over all contexts
  context_node_cursor = problematic_node
  template_id = 0
  while context_node_cursor is not None:

    # 4 skip invalid templates
    validation_result = _validate_template(src_lang, full_ast_text, context_node_cursor, template_id)
    if validation_result is not None:
      templates_dict[template_id] = validation_result
      template_id += 1
      context_node_cursor = context_node_cursor.get_parent()
      continue

    # 5 get the template for the current context
    template_dict = template_tree.get_template_dict_for_node_id(problematic_node.get_id(), context_node_cursor.get_id(), src_lang)

    # Some of the key-value pairs are not used, since we have replaced
    # LLM-based TSP generation by generator-based TSP generation.
    # For example, `templatized_node_ids`, `is_insert_secret_fn`.
    # They can be recovered from `TemplateTree` class and git history.
    templates_dict['context_node_path'] = template_tree.root_node.get_path_to_child(context_node_cursor)
    templates_dict[template_id] = {
      'template_id': template_id,
      'src_lang': src_lang,
      'tar_lang': tar_lang,
      'template_origin': template_dict['template_origin'],
      'context_node_type': context_node_cursor.get_ts_node_type(),
      'context_node_id': context_node_cursor.get_id(),
      'problematic_node_type': problematic_node.get_ts_node_type(),
      'problematic_node_id': problematic_node.get_id(),
      'problematic_node_path': template_dict['problematic_node_path'],
      'is_valid_template': True,
      'is_insert_secret_fn': False,  # always False, unless set by p_generator.generate_tsp_with_generator._is_valid_fuzz_node
      'contexts': parse_raw_contexts(contexts, template_id),
    }

    template_id += 1
    context_node_cursor = context_node_cursor.get_parent()

    # NOTE break for now, save only the first valid template
    break

  templates_dict['num_templates'] = template_id
  return templates_dict


def _validate_template(
  lang: str,
  full_ast_text: list,
  context_node: pds.PirelNode,
  template_id: int
) -> Union[dict, None]:
  '''
  Validate template.
  RETURN None if template is valid, dict with debug information otherwise.
  '''

  reference_tree_full = pds.PirelTree(full_ast_text)
  reference_tree_full._fix_indentation()

  reference_template_node = reference_tree_full.get_node_with_id(context_node.get_id())
  reference_template_text = reference_template_node.get_text()

  if p_utils.does_have_parse_error(reference_template_text, lang):
    return {
      'template_id': template_id,
      'template_origin': reference_template_text,
      'context_node_type': context_node.get_type(),
      'template_origin_node_type': None,
      'is_valid_template': False,
      'error': 'parse error of template_origin'
    }

  reference_template_ast_text, _ = d_ast_parse.parse_text_dbg(reference_template_text, lang, keep_text=True)
  reference_template_tree = pds.PirelTree(reference_template_ast_text)

  error = None
  template_origin_node_type = reference_template_node.get_type()

  if p_utils.does_have_parse_error(reference_template_text, lang):
    error = 'template origin has a parse error when parsed as it is'
  elif len(reference_template_tree.get_root_node().get_children()) > 1:
    error = 'template origin root node contains multiple children nodes'
  elif not context_node.is_type_isomorphic_to(reference_template_tree.get_root_node().get_children()[0]):
    error = 'template origin is not type-isomorphic to the context node'
    template_origin_node_type = reference_template_tree.get_root_node().get_children()[0].get_type()

  # template is good
  if error is None:
    return None

  return {
    'template_id': template_id,
    'template_origin': reference_template_text,
    'context_node_type': context_node.get_type(),
    'template_origin_node_type': template_origin_node_type,
    'is_valid_template': False,
    'error': error
  }


def parse_raw_contexts(contexts: List[dict], template_id: int) -> list:
  '''
  This is a helper function that processes the raw context information
  produced by `d_grammar_expand.TransSession` class to a format that
  suits our goals and needs. The raw context information is "complete",
  in the sense that it precisely points to the problematic node.
  '''
  def _context_signature(context: dict) -> str:
    return str(context)

  def _deduplicate_contexts(contexts: List[dict]) -> List[dict]:
    context_signatures = set()
    unique_contexts = []
    for context in contexts:
      signature = _context_signature(context)
      if signature in context_signatures:
        continue
      context_signatures.add(signature)
      unique_contexts.append(context)
    return unique_contexts

  def _get_parents_list(
    _scptr: List[list],
    _tcptr: List[list],
    template_id: int
  ) -> Tuple[List[str], List[str]]:
    '''
    Skip elements with empty parents list
    RAISE _CptrError due to invalid context (TODO when/why this happens?)
    '''
    assert _scptr[0][0] == 'init', 'sanity check: type of first element should be `init`'
    assert _tcptr[0][0] == 'init', 'sanity check: type of first element should be `init`'
    assert len(_scptr[0][1]) == 1, 'sanity check: there should be one parent in first element'
    assert len(_tcptr[0][1]) == 1, 'sanity check: there should be one parent in first element'
    src_parents, tar_parents = [_scptr[0][1][0]], [_tcptr[0][1][0]]

    if template_id == 0:
      return (src_parents, tar_parents)

    count_parents_added = 0
    for scptr_elem, tcptr_elem in zip(_scptr[1:], _tcptr[1:]):
      assert scptr_elem[0] == 'parent', 'sanity check: type of i-th element should be `parent`'
      assert tcptr_elem[0] == 'parent', 'sanity check: type of i-th element should be `parent`'
      assert len(scptr_elem) == 2, 'sanity check: i-th element should be of size 2'
      assert len(tcptr_elem) == 2, 'sanity check: i-th element should be of size 2'

      # skip elements with empty parents list
      if len(scptr_elem[1]) == 0 or len(tcptr_elem[1]) == 0:
        if len(scptr_elem[1]) != 0:
          raise _CptrError('sanity check: when one of elements has 0 parents, both must have')
        if len(tcptr_elem[1]) != 0:
          raise _CptrError('sanity check: when one of elements has 0 parents, both must have')
        continue

      src_parents.extend(scptr_elem[1])
      tar_parents.extend(tcptr_elem[1])

      count_parents_added += len(scptr_elem[1])
      if count_parents_added >= template_id:
        assert count_parents_added == template_id, 'sanity check: stop in between trans.rules'
        break

    return (src_parents, tar_parents)

  def _process_parents(
    parents: List[str],
    context_copy: List[List[str]],
  ) -> List[List[str]]:
    new_context = []
    # process last parent separately
    for i in range(len(parents) - 1):
      parent = parents[i]
      node_and_prev_siblings = context_copy[i]
      assert parent == node_and_prev_siblings[0], 'sanity check: should not happen, debugging needed'
      new_context.append(node_and_prev_siblings)
    # for last parent, add itself only, do not add its siblings
    new_context.append([context_copy[len(parents) - 1][0]])
    return new_context

  template_contexts = []
  for context in contexts:
    source_context = copy.deepcopy(context['source_context'])
    target_context = copy.deepcopy(context['target_context'])

    # NOTE Translation rules' matcher and expander may contain trees
    # of different sizes. For example, consider the following translation rule:
    # match_expand
    #   (fragment ("py.unary_operator" (str "-") ".") "*")
    #   (fragment ("js.binary_expression" ("js.number" (val "0")) (str "-") ("js.parenthesized_expression" (str "(") ".1" (str ")"))) "*2")
    # the matcher has a depth of 1, and the expander has a depth of 2.
    # We cannot slice expander parents sequence in the middle.
    # `_scptr`, `_tcptr` help us achieve that.
    # For more information, refer to `p_grammar.TransSession.pirel_get_contexts_for_slot`
    # and possibly previous invalid implementations/revisions.
    _scptr = copy.deepcopy(context['_scptr'])
    _tcptr = copy.deepcopy(context['_tcptr'])
    assert len(_scptr) == len(_tcptr), 'sanity check'

    try:
      src_parents, tar_parents = _get_parents_list(_scptr, _tcptr, template_id)
    except _CptrError as err:
      logger.warning(f'skipping context due to {err.__class__.__name__}. Error: {err}')
      continue

    new_source_context = _process_parents(src_parents, source_context)
    new_target_context = _process_parents(tar_parents, target_context)

    template_contexts.append({
      'source_context': new_source_context,
      'target_context': new_target_context,
    })

  assert len(template_contexts) > 0, 'sanity check: due to skipping of some contexts'
  deduplicated_contexts = _deduplicate_contexts(template_contexts)
  return deduplicated_contexts
