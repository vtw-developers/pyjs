import copy
from typing import Callable, List, Optional, Tuple, Union

import d_ast_parse
import d_ast_pretty
import d_grammar_dlmparser as gdp
import d_grammar_rules
import p_consts
import p_data_structures as pds
import p_templates
import p_utils
from d_consts import DEBUG_VERBOSE


logger = p_utils.setup_logger(__name__)


class TranslationRuleNotFoundException(Exception):
  '''
  Exception that is thrown in case DuoGlot does not find a suitable translation rule.

  One use case:
  If this exception is caught, signal a loop for automatic rule inference.
  '''
  def __init__(self, templates_dict: dict) -> None:
    problematic_node_type = templates_dict['problematic_node_type']
    problematic_node_id = templates_dict['problematic_node_id']
    message = f'problematic_node_type="{problematic_node_type}", problematic_node_id={problematic_node_id}'
    super().__init__(message)
    self.templates_dict = templates_dict

  def get_templates_dict(self) -> dict:
    return self.templates_dict


class ContextExtractionException(Exception):
  '''Thrown when there is an error during context extraction'''


class NormalException(Exception):
  '''Exception that is understood (not fatal/unexpected error) and handled elegantly'''


class UnderstoodException(Exception):
  '''Exception that is understood (not fatal/unexpected error), but not handled elegantly'''


class TransSession():

  def __init__(
    self,
    source_code: str,  # program to translate
    source_ast: list,  # list[str, int, list[*]|str], AST of source program
    source_ann: dict,  # boundaries of AST nodes
    source_language_name: str,  # shorthand source language, e.g. 'py'
    target_language_name: str,  # shorthand target language, e.g. 'js'
    target_grammar: dict,  # grammar for target program in some internal representation
    program_str: str,  # raw text of translation rules
    optional_dbg_info_save_func: Callable,
    slot_dedup_enabled: bool
  ):

    # ~~~ this is a critical constant
    self._BACKWARD_MAX_STEP: int = 100

    self._SNAPSHOT_INTERVAL: int = 800
    self._SLOT_DEDUP_ENABLED: bool = slot_dedup_enabled

    # the slot_dedup is only enabled for astnode choices for now.
    # step choices cannot use slot_dedup unless the cache is not on slots, but on slots' ranges.
    # current impl caches a one-to-one mapping from ranges to slots.

    # Okay to expose
    self.source_code = source_code
    self.source_ast = source_ast
    self.source_ann = source_ann
    self.source_language_name = source_language_name
    self.target_language_name = target_language_name
    self.target_grammar = target_grammar
    self.expansion_programs = []  # a list of expansion programs (~~~ a.k.a. translation rules)

    # internals
    self._optional_dbg_info_save_func = optional_dbg_info_save_func
    self._counter_expansion_id: int = 0
    self._counter_slot_id: int = 1
    self._counter_alt_id: int = 1

    self._slot_dict = {
      0: gdp.Slot(
        0,                         # slot_id:      int, index of slot (auto-increment, primary key)
        None,                      # belong_ex_id: int, index of parent slot
        ([self.source_ast], 0, 1)  # range_cursor: Tuple[ [slot AST] , start_inx, end_idx ]
      )
    }

    self._slot_dedup_lookup = {}
    self._slot_expand_info_dict = {} # no direct access

    # is only modified in self._get_or_create_alt_node()
    self._alt_tree_dict = {
      0: self._alt_node_as_dict(
        0,  # alt_id
        0,  # alt_step
        None,  # expansion
        None,  # choose_idx
        None,  # prev_alt_id
        [0],  # todo_slot_ids
        {'count': 0, 'done': False},  # next_choices_status
        {},  # next_alt_choose_dict
        False,  # is_all_rejected
        True  # is_checkpoint
      )
    }  # alt_id -> alt_node

    self._alt_parser_result_dict = {}

    self._alt_parser_dict = {
      0: gdp.DelimitedParser(
        None,  # clone_obj
        self._slot_dict[0].slot_id,  # initial_slot_id
        target_grammar['_initial_prod'],  # initial_prod
        target_grammar,  # grammar
        self.target_language_name,  # target_language_name
        self._optional_dbg_info_save_func  # optional_dbg_info_func
      )
    } # alt_id -> Parser

    self.any_error = False
    self._set_program_str(program_str)

    # TransSession instances internally use `expansion_programs` for translation programs
    # The field below is used only for debugging purposes and can be removed later
    self.translation_rules_str = program_str

    # Stores the last used translation rule.
    # It is used to debug the translation rule in case there is an issue with it.
    # One of the possible issues is corrupted server state (`AssertionError`)
    self._latest_rule_id = None


  # relation:
  #  each slot belongs to an expansion
  #  a fixed list of slots belong to the same expansion
  #  each expansion belong to one slot
  #  multiple expansions can be alternatives of the same slot
  def get_translation(self, choices, auto_backward=True, **kwargs) -> tuple:
    '''
    This is the main method for performing DuoGlot translation.

    RETURN If translation is successful, returns the target program.
    If the translation is not successful, returns `templates_dict`.

    PARAMETERS:
    choices: what rules to apply at each node (if multiple)?
    auto_backward: whether to automatically backtrack if translation fails

    LOCALS:
    current_alt_node_dict: dict ?
    next_alt_node_dict: dict ?
    par_alt_node_dict: dict ?

    NOTE Previously would handle ALL exceptions, now propagates them.
    Known exceptions that are raised:
    - TranslationRuleNotFoundException
    - ContextExtractionException
    - NormalException
    - UnderstoodException
    - AssertionError
    - ...
    '''

    choice_type = choices['type']
    if choice_type == 'STEP':
      choices_dict = {x:y for x, y in choices['choices_list']}
    elif choice_type == 'ASTNODE':
      choices_dict = {tuple(x):y for x, y in choices['choices_list']}

    def _get_or_create_next_alt_inner_fun(alt_node, **kwargs):
      '''
      Read choices object to update which alt_node to get or create next.
      '''
      nonlocal choice_type, choices_dict

      assert choice_type in ['STEP', 'ASTNODE'], 'choice_type must be STEP or ASTNODE'
      assert len(alt_node['todo_slot_ids']) > 0

      slot_expan_idx = 0  # by default, choose the first matched rule (thus, expansion)
      new_step = alt_node['alt_step'] + 1

      if choice_type == 'STEP' and new_step in choices_dict:
        slot_expan_idx = choices_dict[new_step]

      elif choice_type == 'ASTNODE':
        todo_slot_id = alt_node['todo_slot_ids'][0]
        todo_slot = self._slot_dict[todo_slot_id]
        ast_node, start_idx, end_idx = todo_slot.range_cursor
        if new_step == 1:
          assert len(ast_node) == 1
        else:
          ast_id = ast_node[1]
          assert isinstance(ast_id, int), 'ast_id must be an integer'
          key = (ast_id, start_idx, end_idx)
          if key in choices_dict:
            slot_expan_idx = choices_dict[key]

      next_alt_node_dict = self._get_or_create_alt_node(alt_node, slot_expan_idx, **kwargs)
      return next_alt_node_dict

    def _get_nth_parent_inner_fun(alt_node, n):
      if alt_node is None:
        return None
      if n == 0:
        return alt_node
      return _get_nth_parent_inner_fun(self._alt_tree_dict[alt_node['prev_alt_id']], n - 1)

    _allowed_backward_alt_step = 0
    def _backward_alt_next_choice_inner_func(alt_node, child_choose_idx):
      nonlocal _allowed_backward_alt_step, auto_backward, choice_type

      if not auto_backward:
        raise NormalException('Rejection occurred and automatic backwarding is disabled.')

      _allowed_backward_alt_step = max(_allowed_backward_alt_step, alt_node['alt_step'] - self._BACKWARD_MAX_STEP)
      if alt_node['alt_step'] < _allowed_backward_alt_step:
        raise NormalException('Automatic backwarding failed to find alternative choices. (back limit)')

      # checked all possible choices for this node
      next_choices_status = alt_node['next_choices_status']
      if child_choose_idx + 1 >= next_choices_status['count'] and next_choices_status['done']:
        prev_alt_id = alt_node['prev_alt_id']
        if prev_alt_id is None:
          raise NormalException('Automatic backwarding failed to find alternative choices. (back to root)')
        return _backward_alt_next_choice_inner_func(self._alt_tree_dict[prev_alt_id], alt_node['choose_idx'])

      assert choice_type in ['STEP', 'ASTNODE'], 'choice_type must be STEP or ASTNODE'
      new_ch_idx = child_choose_idx + 1
      if choice_type == 'STEP':
        next_step = alt_node['alt_step'] + 1
        return alt_node, next_step, new_ch_idx

      elif choice_type == 'ASTNODE':
        slot_id = alt_node['todo_slot_ids'][0]
        slot_range_cursor = self._slot_dict[slot_id].range_cursor
        next_range_key = (slot_range_cursor[0][1], slot_range_cursor[1], slot_range_cursor[2])
        return alt_node, next_range_key, new_ch_idx

    def _get_alt_parser_result_inner_fun(alt_node):
      try:
        parser_result = self._ensure_parser_result(alt_node)
        return parser_result['is_acceptable'], parser_result['stuck_slot_id'], parser_result['is_done']
      except Exception as err:
        error_alt_parser_result = self._alt_parser_result_dict[alt_node['alt_id']]
        assert error_alt_parser_result['is_error']
        raise err

    current_alt_node_dict = self._alt_tree_dict[0]
    MAX_LOOPCOUNT = 400000  # be cautious, as it may use a lot of memory
    loop_count = 0
    last_checkpoint_step = 0

    try:
      while True:
        loop_count += 1
        assert loop_count < MAX_LOOPCOUNT, 'Loop count exceeded'
        assert len(current_alt_node_dict['todo_slot_ids']) > 0

        # ~~~ this is an important invocation (contains invocation of PiREL)
        next_alt_node_dict = _get_or_create_next_alt_inner_fun(current_alt_node_dict, **kwargs)
        par_alt_node_dict = current_alt_node_dict
        current_alt_node_dict = next_alt_node_dict

        # ~~~ check if the target AST is acceptable
        is_acceptable, stucking_slot_id, is_done = _get_alt_parser_result_inner_fun(current_alt_node_dict)

        if not is_acceptable:
          if par_alt_node_dict['alt_step'] - last_checkpoint_step > self._BACKWARD_MAX_STEP:
            nth_parent = _get_nth_parent_inner_fun(par_alt_node_dict, self._BACKWARD_MAX_STEP)
            if nth_parent is not None:
              self._update_alt_node_as_checkpoint(nth_parent['alt_id'])
              last_checkpoint_step = nth_parent['alt_step']
          current_alt_node_dict, update_key, update_choose_idx = _backward_alt_next_choice_inner_func(par_alt_node_dict, current_alt_node_dict['choose_idx'])
          choices_dict[update_key] = update_choose_idx

        elif len(current_alt_node_dict['todo_slot_ids']) == 0:
          assert is_done
          break

        else:
          # optimization block
          if par_alt_node_dict['alt_step'] - last_checkpoint_step > self._SNAPSHOT_INTERVAL:
            self._update_alt_node_as_checkpoint(par_alt_node_dict['alt_id'])
            last_checkpoint_step = par_alt_node_dict['alt_step']

      tar_ast = self._get_alt_partial_ast(current_alt_node_dict)
      return tar_ast, self._get_alt_debug_history(current_alt_node_dict)

    except Exception as exc:
      # intercept all exceptions and attach debug history
      exc.dbg_history = self._get_alt_debug_history(current_alt_node_dict)
      raise

  def _get_or_create_alt_node(self, prev_alt_node, slot_expan_idx, **kwargs):
    assert len(prev_alt_node["todo_slot_ids"]) > 0

    prev_alt_node_id = prev_alt_node["alt_id"]
    prev_alt_step = prev_alt_node["alt_step"]
    new_node_corres_slot_id = prev_alt_node["todo_slot_ids"][0]

    # 1 expansion does not exist (create and cache it)
    if slot_expan_idx not in prev_alt_node["next_alt_choose_dict"]:

      # 2 ~~~ get expansion
      expansion = self._get_expansion_for_slot(new_node_corres_slot_id, slot_expan_idx)

      # 3 ~~~~~ PiREL template extraction entrypoint
      if expansion is None:
        logger.debug(f'Problematic node found during translation: no translation rule to handle it.')

        skip_template_extraction = kwargs.get('skip_template_extraction', False)
        if skip_template_extraction:
          logger.debug('Skipping template extraction. Just problematic node type and id will be extracted.')
          prob_ntype, prob_nid = self.pirel_get_problematic_node(new_node_corres_slot_id)
          templates_dict = {'problematic_node_type': prob_ntype, 'problematic_node_id': prob_nid}
          raise TranslationRuleNotFoundException(templates_dict)

        templates_dict: dict = self.pirel_get_templates(new_node_corres_slot_id)
        raise TranslationRuleNotFoundException(templates_dict)

      next_choices_status = self._get_expansions_stat_for_slot(new_node_corres_slot_id)
      assert "next_choices_status" in prev_alt_node
      prev_alt_node["next_choices_status"] = next_choices_status

      alt_node = self._alt_node_as_dict(
        self._counter_alt_id,  # alt_id
        prev_alt_step + 1,  # alt_step
        expansion,  # expansion
        slot_expan_idx,  # choose_idx
        prev_alt_node_id,  # prev_alt_id
        self._alt_calc_todo_slots(expansion, prev_alt_node),  # todo_slot_ids
        {"count": 0, "done": False},  # next_choices_status
        {},  # next_alt_choose_dict
        False,  # is_all_rejected
        False  # is_checkpoint
      )

      self._alt_tree_dict[alt_node["alt_id"]] = alt_node
      prev_alt_node["next_alt_choose_dict"][slot_expan_idx] = alt_node["alt_id"]
      self._counter_alt_id += 1

    return self._alt_tree_dict[prev_alt_node["next_alt_choose_dict"][slot_expan_idx]]


  def pirel_get_problematic_node(self, slot_id: int) -> Tuple[str, int]:
    '''
    When translation fails and PiREL is not enabled,
    finds what is id and type of the problematic node.
    RETURN Tuple (problematic_node_id, problematic_node_type)

    Code is taken from `self.pirel_get_templates`
    '''

    # slot is pertinent to the node that cannot be translated
    slot = self._slot_dict[slot_id]
    slot_range_cursor = slot.range_cursor
    slot_child_node_ids = slot.slot_node_ids

    slot_ast = slot_range_cursor[0]  # this is a pure AST node as parsed by d_ast_parse.parse_text_dbg() OR a sub-node
    slot_start_idx = slot_range_cursor[1]
    slot_end_idx = slot_range_cursor[2]

    # 1. identify problematic node
    # idea: it is the first NT node in slot.range_cursor.ast[start_idx, end_idx]
    problem_node_ast = None
    for __cursor_idx in range(slot_start_idx, slot_end_idx):
      problem_node_ast = slot_ast[__cursor_idx]
      if problem_node_ast[1] in slot_child_node_ids:
        break

    problematic_node_type = problem_node_ast[0].split('.')[1]
    problematic_node_id = problem_node_ast[1]
    return problematic_node_type, problematic_node_id


  # ~~~~~ our logic for extracting templates from AST
  def pirel_get_templates(self, slot_id: int):
    '''
    slot_range_cursor:
    Tuple[ AST , start_idx , end_idx ]
    '''
    logger.debug(f'Starting PiREL template extraction.')

    try:
      contexts = self.pirel_get_all_contexts(slot_id)
    except Exception as exc:
      logger.error(f'Error during context extraction: type="{type(exc)}", msg="{str(exc)}"')
      raise ContextExtractionException from exc

    # slot is pertinent to the node that cannot be translated
    slot = self._slot_dict[slot_id]
    slot_range_cursor = slot.range_cursor
    slot_child_node_ids = slot.slot_node_ids

    # this is a pure AST node as parsed by d_ast_parse.parse_text_dbg() OR a sub-node
    slot_ast = slot_range_cursor[0]
    slot_start_idx = slot_range_cursor[1]
    slot_end_idx = slot_range_cursor[2]

    # 1. identify problematic node
    # idea: it is the first NT node in slot.range_cursor.ast[start_idx, end_idx]
    problem_node_ast = None
    for __cursor_idx in range(slot_start_idx, slot_end_idx):
      problem_node_ast = slot_ast[__cursor_idx]
      if problem_node_ast[1] in slot_child_node_ids:
        break

    # full AST information can be leveraged
    full_ast_w_text, ast_annotation = d_ast_parse.parse_text_dbg(self.source_code, self.source_language_name, keep_text=True)

    templates_dict = p_templates.extract_templates(
      problem_node_ast,
      full_ast_w_text,
      ast_annotation,
      self.source_language_name,
      self.target_language_name,
      contexts
    )

    logger.debug(f'PiREL template extraction is complete.')
    return templates_dict


  def pirel_get_all_contexts(self, problematic_slot_id: int):
    '''return a list of unique contexts for problematic node'''

    # 1 get slot ids that are problematic and have the same node type and node id
    problematic_slot_ids = self.pirel_expand_unexpanded_slots_get_problematic_slot_ids(problematic_slot_id)
    problematic_slot_ids = list(set(problematic_slot_ids))  # remove duplicates

    # 2 collect unique contexts
    unique_contexts_dict = {}
    for problematic_slot_id in problematic_slot_ids:
      source_context, target_context, _scptr, _tcptr = self.pirel_get_contexts_for_slot(problematic_slot_id)
      hash_val = str(source_context) + str(target_context)
      if hash_val not in unique_contexts_dict:
        unique_contexts_dict[hash_val] = {
          'source_context': source_context,
          'target_context': target_context,
          '_scptr': _scptr,
          '_tcptr': _tcptr,
        }

    return list(unique_contexts_dict.values())


  def pirel_get_contexts_for_slot(self, problematic_slot_id: int):
    '''
    Return the context of problematic node.
    That is, the sequence of nodes from context node
    to problematic node (in pre-order traversal) for both
    source and target sides.
    This information is useful for post-processing a rule
    in such a way, that allows us to extract the rule
    for the problematic node only (chop-off the context info).

    NOTE this is an early version of the algorithm.
    It skips nodes in cases where the applied rules (expansion)
    are complex.

    PRE1: slot_id in self._slot_dict

    ==== updated docs below
    PRE: slot_id is id of slot with no expansions
    NOTE
    target_context starts with 'unknown', because this method is
    intended to be used with slot that were not expanded
    '''

    assert problematic_slot_id in self._slot_dict

    def _get_slot_by_id(idx: int) -> gdp.Slot:
      return self._slot_dict[idx]

    def _get_expansion_by_id(idx: int) -> gdp.Expansion:
      for _item in self._slot_expand_info_dict.values():
        assert len(_item) == 3
        _expansions, _, _ = _item
        for _exp in _expansions:
          if _exp.ex_id == idx:
            return _exp
      raise RuntimeError('Expansion not found, should not happen')

    def _get_node_type_from_slot(slot: gdp.Slot) -> str:
      slot_range_cursor = slot.range_cursor
      slot_child_node_ids = slot.slot_node_ids

      slot_ast = slot_range_cursor[0]
      slot_start_idx = slot_range_cursor[1]
      slot_end_idx = slot_range_cursor[2]

      node_ast = None
      for _cursor_idx in range(slot_start_idx, slot_end_idx):
        node_ast = slot_ast[_cursor_idx]
        if node_ast[1] in slot_child_node_ids:
          break
      assert node_ast is not None

      slot_type = node_ast[0]
      return slot_type

    def _get_source_target_paths(expansion: gdp.Expansion, previous_slot: gdp.Slot) -> list:
      assert previous_slot in expansion.slots

      # ".1", ".2", "*3", etc
      slot_name = expansion.slot_names[expansion.slots.index(previous_slot)]

      # extract context from rule
      rule_id = expansion.notes['rule_id']
      trans_rule = self.expansion_programs[rule_id]
      match_pattern = trans_rule['match']  # aka source pattern
      expand_pattern = trans_rule['expand']  # aka target pattern

      match_tree = pds.PatternTree(match_pattern, self.source_language_name)
      expand_tree = pds.PatternTree(expand_pattern, self.target_language_name)
      phnode_match = match_tree.get_node_with_type(slot_name)
      phnode_expand = expand_tree.get_node_with_type(slot_name)

      source_path = phnode_match.get_path_to_root_source(expansion)
      target_path = phnode_expand.get_path_to_root_target(expansion, self._slot_expand_info_dict)

      return source_path, target_path

    def _update_contexts(context: List[list], paths: list):
      '''
      `context` has two elements:
      1. parent of the node (a single string in a list)
      2. previous siblings of the node (list of strings)

      NOTE writes to `context`
      '''
      for sibling in paths[-1]:
        context[-1].append(sibling)
      for parent in reversed(paths[:-1]):
        context.append(parent)

    def _update_contexts_per_trans_rule(context: List[list], paths: list):
      '''
      NOTE writes to `context`
      '''
      # parent of previous
      parents = []
      for e in reversed(paths[:-1]):
        parents.append(e[0])
      context.append(['parent', parents])

    source_context = []
    target_context = []
    source_context_per_trans_rule = []
    target_context_per_trans_rule = []

    # 1
    # Since we start with the problematic node,
    # obtain its type first.
    # The corresponding type in the target side is 'unknown',
    # because we don't know what problematic node converts to.

    problematic_slot : gdp.Slot = _get_slot_by_id(problematic_slot_id)
    problematic_slot_type : str = _get_node_type_from_slot(problematic_slot)

    # NOTE what if the slot is partially matched? -> get only the top node in rule
    # NOTE can problematic node have a sibling?
    source_context.append([problematic_slot_type])
    target_context.append(['unknown'])
    # NOTE these two are needed for better context construction:
    # for some cases, chain of parents may differ in length for source
    # and target contexts. Instead of blindly picking N parents above,
    # pick them based on (please read the source code, I am sorry)
    source_context_per_trans_rule.append(('init', [problematic_slot_type]))
    target_context_per_trans_rule.append(('init', ['unknown']))

    # 2
    # set up transduction tree cursors
    # iterate up over slot-expansion pairs
    previous_slot = problematic_slot
    cursor_expansion_id : Union[int, None] = problematic_slot.belong_ex_id
    # hit the root node (unlikely at this step)
    if cursor_expansion_id is None:
      return source_context, target_context, source_context_per_trans_rule, target_context_per_trans_rule
    cursor_expansion = _get_expansion_by_id(cursor_expansion_id)
    cursor_slot_id = cursor_expansion.corres_slot_id
    cursor_slot = _get_slot_by_id(cursor_slot_id)

    # 3
    # iterating up the transduction tree
    while True:

      source_paths, target_paths = _get_source_target_paths(cursor_expansion, previous_slot)
      _update_contexts(source_context, source_paths)
      _update_contexts(target_context, target_paths)
      _update_contexts_per_trans_rule(source_context_per_trans_rule, source_paths)
      _update_contexts_per_trans_rule(target_context_per_trans_rule, target_paths)

      # update cursors
      previous_slot = cursor_slot
      cursor_expansion_id = cursor_slot.belong_ex_id
      # hit the root node
      if cursor_expansion_id is None:
        break
      cursor_expansion = _get_expansion_by_id(cursor_expansion_id)
      cursor_slot_id = cursor_expansion.corres_slot_id
      cursor_slot = _get_slot_by_id(cursor_slot_id)

    return source_context, target_context, source_context_per_trans_rule, target_context_per_trans_rule


  def pirel_expand_unexpanded_slots_get_problematic_slot_ids(self, problematic_slot_id: int):
    ''''''
    def _get_slot_root_node_id(slot: gdp.Slot) -> int:
      '''extract useful information from slot'''
      slot_range_cursor = slot.range_cursor
      slot_child_node_ids = slot.slot_node_ids

      slot_ast = slot_range_cursor[0]
      slot_start_idx = slot_range_cursor[1]
      slot_end_idx = slot_range_cursor[2]

      node_ast = None
      for _cursor_idx in range(slot_start_idx, slot_end_idx):
        node_ast = slot_ast[_cursor_idx]
        if node_ast[1] in slot_child_node_ids:
          break
      assert node_ast is not None

      slot_node_id = node_ast[1]
      return slot_node_id

    def _get_slot_root_node_type(slot: gdp.Slot) -> str:
      '''extract useful information from slot'''
      slot_range_cursor = slot.range_cursor
      slot_child_node_ids = slot.slot_node_ids

      slot_ast = slot_range_cursor[0]
      slot_start_idx = slot_range_cursor[1]
      slot_end_idx = slot_range_cursor[2]

      node_ast = None
      for _cursor_idx in range(slot_start_idx, slot_end_idx):
        node_ast = slot_ast[_cursor_idx]
        if node_ast[1] in slot_child_node_ids:
          break
      assert node_ast is not None

      slot_type = node_ast[0]
      return slot_type

    def _get_slot_parent_expansion(slot: gdp.Slot) -> Union[gdp.Expansion, None]:
      '''
      get parent expansion of slot (up)
      a slot belongs to exactly ONE expansion
      '''
      for expansions, is_finished, expansion_gen in self._slot_expand_info_dict.values():
        for expansion in expansions:
          if expansion.ex_id == slot.belong_ex_id:
            return expansion

      # reaching this line means we reached root slot (which has no parent expansion)
      return None

    def _get_slot_possible_expansions(slot: gdp.Slot) -> Union[List[gdp.Expansion], None]:
      '''
      return all possible expansions that might be created from this slot (down)

      might return
      1. None - in case expansions were not generated for this slot
      2. empty list - no translation rule matched for slot
      3. non-empty list - expansions
      '''

      slot_id = slot.slot_id

      # slot was created, but expansions for this slot were not
      if slot_id not in self._slot_expand_info_dict:
        return None

      return self._slot_expand_info_dict[slot_id][0]

    def _get_expansion_root_node_type(expansion: gdp.Expansion) -> str:
      ''''''
      expansion_fragment = expansion.expan_fragment

      # TODO changes depending on the size of expansion_fragment
      expansion_type = expansion_fragment[1][0].strip('"')

      return expansion_type

    def _get_expansion_parent_slot(expansion: gdp.Expansion) -> gdp.Slot:
      '''
      get the slot from which this expansion was created (up)
      an expansion can be created from exactly ONE slot
      '''
      parent_slot_id = expansion.corres_slot_id

      # TODO does it always exist?
      return self._slot_dict[parent_slot_id]

    def _get_expansion_created_slots(expansion: gdp.Expansion) -> List[gdp.Slot]:
      '''
      return a list of all slots that were created by this expansions
      the list might be empty. in fact, it is empty for translation rules that create
      only terminals on the target side
      '''
      # might contain None (in cases where a rule matches an empty AST)
      expansion_slots_all = expansion.slots
      expansion_slots = list(filter(lambda x: isinstance(x, gdp.Slot), expansion_slots_all))
      return expansion_slots

    def _traverse_expand_unexpanded_slots_down_and_collect_problematic_slots(slot: gdp.Slot, from_expansion: gdp.Expansion, depth: int):
      '''
      when translation fails, complete generating expansions for all slots
      NOTE this has to be done, because when translation stops at a slot,
      some slots (to be precise, the ones that come after the problematic slot in
      pre-order traversal?) are kept unexpanded (i.e. no expansions are created
      from them)
      '''

      nonlocal DEPTH_SPAN
      nonlocal _MIN_DEPTH_PROB_SLOT

      # stop the recursion
      if _MIN_DEPTH_PROB_SLOT != -1 and depth > _MIN_DEPTH_PROB_SLOT + DEPTH_SPAN:
        return

      # 0 check if slot is problematic
      nonlocal problematic_slots
      nonlocal problematic_slot_node_type
      nonlocal problematic_slot_node_id
      if _get_slot_root_node_type(slot) == problematic_slot_node_type and _get_slot_root_node_id(slot) == problematic_slot_node_id:

        # record the depth of the first problematic slot
        if _MIN_DEPTH_PROB_SLOT == -1:
          _MIN_DEPTH_PROB_SLOT = depth

        problematic_slots.append(slot)

      # 1 get all expansions for this slot
      slot_possible_expansions = _get_slot_possible_expansions(slot)

      # case 1: expansions were not created from this slot -> run `self._get_expansion_for_slot()`
      if slot_possible_expansions is None:
        slot_id : int = slot.slot_id
        slot_expan_idx = 0  # choose i-th in case of multiple expansions

        # NOTE might return None
        expansion = self._get_expansion_for_slot(slot_id, slot_expan_idx)

        if expansion is not None:
          _traverse_expand_unexpanded_slots_down_and_collect_problematic_slots(slot, from_expansion, depth=depth+1)

      # case 2: no translation rule to translate the slot -> can stop
      elif len(slot_possible_expansions) == 0:
        pass

      # case 3: iterate expansions
      else:
        for possible_expansion in slot_possible_expansions:

          # 2 get all slots created by `possible_expansion`
          possible_expansion_slots = _get_expansion_created_slots(possible_expansion)

          # 3 for each slot, recurse down
          for possible_expansion_slot in possible_expansion_slots:
            _traverse_expand_unexpanded_slots_down_and_collect_problematic_slots(possible_expansion_slot, possible_expansion, depth=depth+1)

    # NOTE not used here, for future reference
    def _traverse_slot_expansion_down(slot: gdp.Slot, expansion: gdp.Expansion):
      '''
      PARAMS
      slot:

      expansion:
      an expansion that was created from `slot`
      '''
      nonlocal all_path_segments

      # 1 do sth with `slot`
      # 2 do sth with `expansion`
      slot_node_type = _get_slot_root_node_type(slot)
      slot_node_id = _get_slot_root_node_id(slot)
      expansion_type = _get_expansion_root_node_type(expansion)
      slot_id = slot.slot_id
      expansion_id = expansion.ex_id
      all_path_segments.append(f'down s{slot_id}_{slot_node_type}_{slot_node_id} -> e{expansion_id}_{expansion_type}')

      # 3 get all slots created by `expansions` (down)
      expansion_slots = _get_expansion_created_slots(expansion)

      # 4 for each slot, get all possible expansions
      for expansion_slot in expansion_slots:
        expansion_slot_node_type = _get_slot_root_node_type(expansion_slot)
        expansion_slot_node_id = _get_slot_root_node_id(expansion_slot)
        expansion_slot_id = expansion_slot.slot_id
        possible_expansion_slot_expansions = _get_slot_possible_expansions(expansion_slot)

        # case 1: expansions were not created yet
        if possible_expansion_slot_expansions is None:
          all_path_segments.append(f'down s{expansion_slot_id}_{expansion_slot_node_type}_{expansion_slot_node_id} -> ?')
          continue

        # case 2: expansions were attempted
        if len(possible_expansion_slot_expansions) == 0:
          all_path_segments.append(f'down s{expansion_slot_id}_{expansion_slot_node_type}_{expansion_slot_node_id} -> x')
          continue

        for possible_expansion_slot_expansion in possible_expansion_slot_expansions:

          # for each [slot, expansion] pair, recurse
          _traverse_slot_expansion_down(expansion_slot, possible_expansion_slot_expansion)

    # NOTE not used here, for future reference
    def _traverse_slot_expansion_down_from_start():
      ''''''
      start_slot_id = 0
      start_slot = self._slot_dict[start_slot_id]
      possible_expansions = _get_slot_possible_expansions(start_slot)

      assert possible_expansions is not None
      assert len(possible_expansions) > 0

      for possible_expansion in possible_expansions:
        _traverse_slot_expansion_down(start_slot, possible_expansion)

    # NOTE not used here, for future reference
    def _traverse_slot_expansion_up(slot: gdp.Slot, from_expansion: Union[gdp.Expansion, None]):
      '''
      PARAMS
      from_expansion:
      an expansion from which we arrived at `slot` when going up.
      essentially, `from_expansion` is an expansion that was created from `slot`.

      TERMS
      parent_expansion
      grand_parent_slot
      '''
      nonlocal all_path_segments

      # 1 do sth with slot
      slot_node_type = _get_slot_root_node_type(slot)
      slot_node_id = _get_slot_root_node_id(slot)
      from_expansion_type = _get_expansion_root_node_type(from_expansion) if from_expansion is not None else 'x'
      slot_id = slot.slot_id
      from_expansion_id = from_expansion.ex_id if from_expansion is not None else ''
      all_path_segments.append(f'up s{slot_id}_{slot_node_type}_{slot_node_id} -> e{from_expansion_id}_{from_expansion_type}')

      # 4 get the expansion that this slot belongs to
      parent_expansion = _get_slot_parent_expansion(slot)

      # the `slot` is the root slot
      if parent_expansion is None:
        return

      # 5 get the slot from which parent_expansion was created
      grand_parent_slot = _get_expansion_parent_slot(parent_expansion)

      # 6 recurse into grand_parent_slot
      _traverse_slot_expansion_up(grand_parent_slot, parent_expansion)

    # 0 temporary list needed for some inner methods here
    # inner methods are stored for future reference, safe to remove now
    all_path_segments = []

    # 1 some information on problematic node
    problematic_slot : gdp.Slot = self._slot_dict[problematic_slot_id]
    problematic_slot_node_type : str = _get_slot_root_node_type(problematic_slot)
    problematic_slot_node_id : int = _get_slot_root_node_id(problematic_slot)
    problematic_slots : List[gdp.Slot] = []  # all slots that point to problematic node

    # 2 expand all unexpanded slots and collect problematic slots

    # these two control the depth of recursion
    _MIN_DEPTH_PROB_SLOT = -1
    DEPTH_SPAN = 3

    start_slot_id = 0
    start_slot : gdp.Slot = self._slot_dict[start_slot_id]
    _traverse_expand_unexpanded_slots_down_and_collect_problematic_slots(start_slot, None, depth=0)

    # 3
    problematic_slot_ids = [slot.slot_id for slot in problematic_slots]
    return problematic_slot_ids


  def _get_expansion_for_slot(self, slot_id: int, idx: int) -> Union[None, gdp.Expansion]:
    '''
    ~~~ if this function returns None, it means that DuoGlot failed to find a rule for translation

    call stack (most recent on top):
    _get_expansion_for_slot()       <- this
    _get_or_create_alt_node()
    _get_or_create_next_alt_inner_fun()
    get_translation()               # inside an expand loop
    '''
    slot = self._slot_dict[slot_id]

    # 1 check cache
    if slot_id not in self._slot_expand_info_dict:
      self._slot_expand_info_dict[slot_id] = [
        [],  # expan_list
        False,  # is_done
        self._possible_expansion_iter_gen(slot)  # iterobj
      ]

    expan_list, is_done, iterobj = self._slot_expand_info_dict[slot_id]

    # 2 expansion exists in cache
    if idx < len(expan_list):
      return expan_list[idx]

    # TODO debug this location: when is it reached?
    if is_done:
      return None

    # 3 find all expansions
    try:
      while len(expan_list) < idx + p_consts.MAX_NUM_ALTERNATIVE_EXPANSIONS:
        next_expansion: gdp.Expansion = next(iterobj)
        assert next_expansion is not None
        expan_list.append(next_expansion)
    except StopIteration:
      self._slot_expand_info_dict[slot_id][1] = True
      self._slot_expand_info_dict[slot_id][2] = None

    # 4 requested expansion idx exists
    if idx < len(expan_list):
      return expan_list[idx]

    # 5 requested expansion idx doesn't exist
    return None


  def _possible_expansion_iter_gen(self, slot):
    if DEBUG_VERBOSE > 0: print(f"_possible_expansion_iter_gen slot: ({slot})")

    choose_idx = 0
    # iterate over all translation rules (a.k.a. expansion programs) in a natural order (as provided in the text field)
    # if a rule matches a 'slot', get an Expansion object and yield it (generator)
    # generator is called in a loop
    # 3 is hard-coded in _get_expansion_for_slot()
    for rule_id in range(len(self.expansion_programs)):
      me_prog = self.expansion_programs[rule_id]
      ruletype = me_prog["type"]
      match = me_prog["match"]
      expand = me_prog["expand"]
      flag_dict = me_prog["flags"] if ruletype == "ext_match_expand" else None

      # try the matcher. If true, return an expansion object
      # expansion is either a None (no match for a given rule_id)
      #              OR     a gdp.Expansion (match exists)
      expansion = self._try_get_expansion_if_match_on_slot(
        slot,  # slot
        rule_id,  # rule_id
        ruletype,  # m_ruletype
        match,  # m_match
        expand,  # m_expand
        flag_dict,  # m_flag_dict
        {"choose_idx": choose_idx}  # notes
      )

      if expansion is not None:
        if DEBUG_VERBOSE > 0: print("# _possible_expansion_iter_gen matched!", slot, expansion)
        yield expansion
        choose_idx += 1

    return None


  # if successful, this function should return an expand object
  def _try_get_expansion_if_match_on_slot(
    self,
    slot: gdp.Slot,
    rule_id: int,
    m_ruletype: str,
    m_match: list,
    m_expand: list,
    m_flag_dict: Optional[dict],
    notes: dict
  ):
    '''
    PARAMETERS:
    slot:        d_grammar_dlmparser.Slot
    rule_id:     int (natural index of translation rule in the ruleset, a.k.a. expansion_programs)
    m_ruletype:  str (e.g. `match_expand`)
    m_match:     list (a type+rule that is matched against source AST)
    m_expand:    list (a type+rule that is matched against target AST)
    m_flag_dict: dict (additional flags for the rule, only for `ext_match_expand` rules)

    LOCALS:
    m_matcher: a source AST matching rule itself -> ['"py.module"', '"*"']
    '''

    def _try_match_rec_inner_fun(
      range_cursor: tuple,
      range_cursor_idx: int,
      matcher: list,
      matcher_idx: int
    ) -> bool:
      '''
      PARAMETERS:
      range_cursor:          Slot.range_cursor           Tuple[ List[src_ast] , int , int ]
      range_cursor_idx:      int                         start index in the AST list
      matcher:               list                        [['"py.argument_list"', '"*"'], '"*"']
      matcher_idx:           int                         index in the matcher

      LOCALS:
      cur_matcher_elem:      list                        ['"py.argument_list"', '"*"']
      matcher_operator:      str                         '"py.argument_list"'  # with double quotes as in rules
      cur_matcher_type:      str                         'py.argument_list'  # without double quotes

      returns bool
      '''

      nonlocal flag_ext_rule
      nonlocal matching_ids, slot_cursors, matching_values, matching_strs
      nonlocal matching_anynts, matching_liststrs, matching_annos

      rc_ast = range_cursor[0]
      rc_start_idx = range_cursor[1]
      rc_end_idx = range_cursor[2]

      # base case: reached the end of cursor and matcher
      if range_cursor_idx >= rc_end_idx and matcher_idx >= len(matcher):
        return True

      # base case: reached the end of matcher
      # the rest of the cursor must all be terminals
      if matcher_idx >= len(matcher):
        for rc_idx in range(range_cursor_idx, rc_end_idx):
          if not isinstance(rc_ast[rc_idx], str):
            return False
        return True

      assert len(matcher) > 0, 'matcher is empty'
      cur_matcher_elem = matcher[matcher_idx]

      # base case: "*" matcher
      if cur_matcher_elem == '"*"':
        # all the rest is a cursor
        slot_cursors.append((rc_ast, range_cursor_idx, rc_end_idx))
        # nothing to update for matching ids
        return True

      # "." matcher
      if cur_matcher_elem == '"."':
        # everything until the next NT is a cursor
        # everything after the next NT would be the rest to match
        split_idx = None  # idx of node right after the NT
        for rc_idx in range(range_cursor_idx, rc_end_idx):
          if _is_elem_NT(rc_ast[rc_idx]):
            split_idx = rc_idx + 1
            break

        # NT not found
        if split_idx is None:
          return False

        # NT found, cursor ends with NT
        slot_cursors.append((rc_ast, range_cursor_idx, split_idx))
        return _try_match_rec_inner_fun(range_cursor, split_idx, matcher, matcher_idx + 1)

      # "_val_" matcher
      if cur_matcher_elem == '"_val_"':
        assert len(matcher) == 1, '_val_ must be the only element in matcher'
        assert len(rc_ast) == 3, 'range cursor must contain 3 elements for _val_ matcher'
        assert (rc_end_idx - rc_start_idx) == 1, 'range cursor indices must be consecutive for _val_ matcher'
        assert range_cursor_idx == 2, 'range cursor index must be 2 for _val_ matcher'
        matching_values.append(rc_ast[2])
        return True

      # "_str_" matcher
      if cur_matcher_elem == '"_str_"':
        if range_cursor_idx >= rc_end_idx:
          return False  # TODO out of length is failed to match
        cur_range_elem = rc_ast[range_cursor_idx]
        if not isinstance(cur_range_elem, str):
          return False
        matching_strs.append(cur_range_elem)
        return _try_match_rec_inner_fun(range_cursor, range_cursor_idx + 1, matcher, matcher_idx + 1)

      # "_liststr_" matcher
      if cur_matcher_elem == '"_liststr_"':
        assert flag_ext_rule, '_liststr_ can be used only in ext_match_expand rules'
        tmp_rc_idx = range_cursor_idx
        temp_liststr = []
        while True:
          if tmp_rc_idx >= rc_end_idx:
            break
          cur_range_elem = rc_ast[tmp_rc_idx]
          if isinstance(cur_range_elem, str):
            temp_liststr.append(cur_range_elem)
            tmp_rc_idx += 1
          else:
            break
        matching_liststrs.append(temp_liststr)
        return _try_match_rec_inner_fun(range_cursor, tmp_rc_idx, matcher, matcher_idx + 1)

      # "_anno_" matcher
      if cur_matcher_elem == '"_anno_"':  # TODO "anno" ?
        cur_range_elem = rc_ast[range_cursor_idx]
        if not isinstance(cur_range_elem, list):
          raise UnderstoodException("_anno_ meet none-annotation element: Not a list.")
        if cur_range_elem[0] != "anno":
          raise UnderstoodException("_anno_ meet none-annotation element: elem head: " + cur_range_elem[0])
        matching_annos.append(cur_range_elem)
        return _try_match_rec_inner_fun(range_cursor, range_cursor_idx + 1, matcher, matcher_idx + 1)

      # at this point, checked all possible options for cur_matcher_elem being a string
      # it must be a list now -> non-terminal
      assert isinstance(cur_matcher_elem, list), 'cur_matcher_elem must be a list at this point'
      matcher_operator = cur_matcher_elem[0]

      # reached the end of range cursor
      if range_cursor_idx >= rc_end_idx:
        if matcher_operator == "val" or matcher_operator == "str" or matcher_operator.startswith('"'):
          return False
        if matcher_operator == "nostr":
          return _try_match_rec_inner_fun(range_cursor, range_cursor_idx, matcher, matcher_idx + 1)
        raise RuntimeError("UNEXPECTED range_cursor_idx out of length in _try_match_rec_inner_fun")

      # e.g. ['val', '"max"']
      if matcher_operator == "val":
        assert len(cur_matcher_elem) == 2, 'val matcher must have exactly 2 elements'
        assert len(rc_ast) == 3, 'range cursor must contain 3 elements for val matcher'
        assert (rc_end_idx - rc_start_idx) == 1, 'range cursor indices must be consecutive for val matcher'
        assert range_cursor_idx == 2, 'range cursor index must be 2 for val matcher'
        rc_val_val = rc_ast[range_cursor_idx]
        if not isinstance(rc_val_val, str) and not isinstance(rc_val_val, int) and not isinstance(rc_val_val, float):
          return False
        matcher_val_val = cur_matcher_elem[1]
        if str(rc_val_val) == str(matcher_val_val):
          return True
        return False

      # e.g. ['str', '"def"']
      if matcher_operator == 'str':
        assert len(cur_matcher_elem) == 2, 'str matcher must have exactly 2 elements'
        rc_str_val = rc_ast[range_cursor_idx]

        # @satbek: skip `anno` in range_cursor when it's matched by `str`
        # when translation rule for string does not have "anno" but the source AST has it
        if isinstance(rc_str_val, list) and len(rc_str_val) > 0 and rc_str_val[0] == 'anno':
          return _try_match_rec_inner_fun(range_cursor, range_cursor_idx + 1, matcher, matcher_idx)

        if not isinstance(rc_str_val, str):
          return False
        matcher_str_val = cur_matcher_elem[1]
        if str(rc_str_val) != str(matcher_str_val):
          return False
        return _try_match_rec_inner_fun(range_cursor, range_cursor_idx + 1, matcher, matcher_idx + 1)

      # e.g. ['nostr']
      if matcher_operator == 'nostr':
        assert len(cur_matcher_elem) == 1, 'nostr matcher must have exactly 1 element'
        if isinstance(rc_ast[range_cursor_idx], str):
          return False
        return _try_match_rec_inner_fun(range_cursor, range_cursor_idx, matcher, matcher_idx + 1)

      # e.g. ['anno' ['"stype"' '""'] ['"quote"' '"\'"']]
      if matcher_operator == 'anno':
        cur_range_elem = rc_ast[range_cursor_idx]
        if not isinstance(cur_range_elem, list):
          raise UnderstoodException('(anno ...) meet none-annotation element: Not a list.')
        if cur_range_elem[0] != 'anno':
          raise UnderstoodException('(anno ...) meet none-annotation element: elem head: ' + cur_range_elem[0])
        if not self.is_anno_compatible(cur_matcher_elem, cur_range_elem):
          return False
        return _try_match_rec_inner_fun(range_cursor, range_cursor_idx + 1, matcher, matcher_idx + 1)

      # not special operators, must be grammar NT constructs
      assert matcher_operator.startswith('"'), 'matcher_operator must start with a double quote here'
      cur_matcher_type = matcher_operator[1:-1]  # remove double quotes
      assert cur_matcher_type != "fragment" and cur_matcher_type != "anno"

      for rc_idx in range(range_cursor_idx, rc_end_idx):
        rc_elem = rc_ast[rc_idx]

        # rc_elem is a terminal, but we are matching against a nonterminal
        if isinstance(rc_elem, str):
          continue
        # we are currently matching against NT, if anno wasn't captured earlier, it will be skipped
        if rc_elem[0] == "anno":
          continue

        assert _is_elem_NT(rc_elem), 'rc_elem must be a non-terminal here'
        rc_elem_type = rc_elem[0]
        is_direct_match = rc_elem_type == cur_matcher_type
        is_arbitrarynt_match = cur_matcher_type == "_anynt_"

        # match
        if is_direct_match or (is_arbitrarynt_match and flag_ext_rule):
          if is_arbitrarynt_match:
            assert flag_ext_rule, 'only ext_match_expand rules can use _anynt_ matcher'
            matching_anynts.append(f'"{rc_elem_type}"')

          # type match, add matching id
          matching_ids.append(rc_elem[1])

          # check if the matching element is matched
          is_elem_matching = _try_match_rec_inner_fun((rc_elem, 2, len(rc_elem)), 2, cur_matcher_elem[1:], 0)
          if not is_elem_matching:
            return False
          return _try_match_rec_inner_fun(range_cursor, rc_idx + 1, matcher, matcher_idx + 1)

        return False

      # no match or mismatch
      return False

    self._latest_rule_id = rule_id  # just for the record

    flag_ext_rule = m_ruletype == "ext_match_expand"
    m_range_cursor = slot.range_cursor
    m_matcher = [m_match]
    if m_match[0] == "fragment":
      m_matcher = m_match[1:]

    matching_ids = []
    slot_cursors = []
    matching_values = []
    matching_strs = []
    matching_anynts = []
    matching_liststrs = []
    matching_annos = []

    is_matched = _try_match_rec_inner_fun(
      m_range_cursor,  # range_cursor
      m_range_cursor[1],  # range_cursor_idx
      m_matcher,  # matcher
      0  # matcher_idx
    )

    if not is_matched:
      return None

    new_notes = copy.copy(notes)
    new_notes["rule_id"] = rule_id

    return self._create_expansion(
      slot.slot_id,  # corres_slot_id
      m_expand,  # m_expand
      matching_ids,  # matching_ids
      slot_cursors,  # slot_cursors
      matching_values,  # matching_values
      matching_strs,  # matching_strs
      matching_anynts,  # matching_anynts
      matching_liststrs,  # matching_liststrs
      matching_annos,  # matching_annos
      new_notes  # notes
    )


  def is_anno_compatible(self, matcher_anno: list, range_anno: list) -> bool:
    matcher_anno_dict = {x[0]:x[1] for x in matcher_anno[1:]}
    range_anno_dict = {x[0]:x[1] for x in range_anno[1:]}
    for key in matcher_anno_dict:
      if key not in range_anno_dict:
        return False
      if matcher_anno_dict[key] != range_anno_dict[key]:
        return False
    return True

  @classmethod
  def _pretty_range_cursor(cls, range_cursor):
    additional_info = []
    for idx in range(range_cursor[1], range_cursor[2]):
      cursor_elem = range_cursor[0][idx]
      if isinstance(cursor_elem, list) and len(cursor_elem) > 0:
        additional_info.append(str(cursor_elem[0]))
      elif isinstance(cursor_elem, str):
        additional_info.append("str:" + cursor_elem)
      elif isinstance(cursor_elem, int):
        additional_info.append("int:" + str(cursor_elem))
      else:
        print("# ERROR!", cursor_elem)
        assert False
    return f"(len={str(len(range_cursor[0]))} start={range_cursor[1]} end={range_cursor[2]} {additional_info}))"

  def _create_expansion(
    self,
    corres_slot_id,
    m_expand,
    matching_ids,
    slot_cursors,
    matching_values,
    matching_strs,
    matching_anynts,
    matching_liststrs,
    matching_annos,
    notes=None
  ):
    self._counter_expansion_id += 1
    return gdp.Expansion(
      self._counter_expansion_id,  # ex_id
      corres_slot_id,  # corres_slot_id
      m_expand,  # expand
      matching_ids,  # matching_node_ids
      slot_cursors,  # src_slot_cursors
      matching_values,  # matching_values
      matching_strs,  # matching_strs
      matching_anynts,  # matching_anynts
      matching_liststrs,  # matching_liststrs
      matching_annos,  # matching_annos
      lambda ex_id, cursor : self._create_or_get_slot(ex_id, cursor),  # slot_create_func
      notes  # notes
    )

  def _create_or_get_slot(self, belong_ex_id, range_cursor):
    ast_id = range_cursor[0][1]
    assert isinstance(ast_id, int)
    start_idx = range_cursor[1]
    end_idx = range_cursor[2]

    if self._SLOT_DEDUP_ENABLED:
      astid_dict = None
      if ast_id in self._slot_dedup_lookup:
        astid_dict = self._slot_dedup_lookup[ast_id]
        if (start_idx, end_idx) in astid_dict:
          return astid_dict[(start_idx, end_idx)]
      else:
        astid_dict = {}
        self._slot_dedup_lookup[ast_id] = astid_dict

    self._counter_slot_id += 1
    new_slot = gdp.Slot(self._counter_slot_id, belong_ex_id, range_cursor)
    self._slot_dict[self._counter_slot_id] = new_slot

    if self._SLOT_DEDUP_ENABLED:
      # add to cache
      astid_dict[(start_idx, end_idx)] = new_slot

    return new_slot


  def _get_expansions_stat_for_slot(self, slot_id):
    assert slot_id in self._slot_expand_info_dict
    expan_list, is_done, _ = self._slot_expand_info_dict[slot_id]
    return {"count":len(expan_list), "done":is_done}

  def _alt_node_as_dict(
    self,
    alt_id,
    alt_step,
    expansion,
    choose_idx,
    prev_alt_id,
    todo_slot_ids,
    next_choices_status,
    next_alt_choose_dict,
    is_all_rejected,
    is_checkpoint
  ):
    return {
      "alt_id": alt_id,
      "alt_step": alt_step,
      "expansion": expansion,
      "choose_idx": choose_idx,
      "prev_alt_id": prev_alt_id,
      "todo_slot_ids": todo_slot_ids,
      "next_choices_status": next_choices_status,
      "next_alt_choose_dict": next_alt_choose_dict,
      "is_all_rejected": is_all_rejected,
      "is_checkpoint": is_checkpoint
    }

  def _alt_calc_todo_slots(self, expansion: gdp.Expansion, prev_alt_node):
    # todo slot dedup impl here? If dedup is on for the whole transsession, then this expansion and its corresponding slot must be unique.
    # can unique expansion/slot produce duplicated children slots? Should be yes.
    # But can the duplicated children slots appear in the same transduction history?
    # (only slots/expansions along a specific transduction history is book-keeped in transducer)
    # Not possible in current transducer impl. because matches inside an expansion are exclusive.
    # If matches are not exclusive, [1] + 2   and [1 +] 2 can be slot 1:([1]) slot 2:([1 +]). Another expansion on slot 2 break it down to [1] and [+]
    # will be unaware that [1] is already handled.
    # If we keep duplicated todo slots, will they affect the transduction?
    old_todo_slot_ids = prev_alt_node["todo_slot_ids"]
    prepend_ids = [x.slot_id for x in expansion.slots if x is not None]
    return prepend_ids + old_todo_slot_ids[1:]


  def _ensure_parser_result(self, alt_node):
    '''
    make sure the parser result is set.
    NOTE: parser_result might be error
    TODO what this method does?
    '''

    alt_id = alt_node["alt_id"]

    # 1 exists in cache (@satbek)
    if alt_id in self._alt_parser_result_dict:
      return self._alt_parser_result_dict[alt_id]

    # 2 does not exist in cache (@satbek)
    try:
      # fetch the previous parser (move or clone from the last checkpoint and move) and run it
      prev_alt_id = alt_node["prev_alt_id"]
      fetched_parser = self._fetch_parser(prev_alt_id)
      expansion = alt_node["expansion"]

      # ~~~ main work
      is_accepted, dbg_info = fetched_parser.add_expansion_parse_until_stuck(expansion)

      parser_result = self._parser_result_as_dict(
        is_accepted,  # is_acceptable
        fetched_parser.last_time_parsing_done,  # is_done
        False,  # is_error
        dbg_info,  # dbg_info
        fetched_parser.last_time_stuck_slot_id  # stuck_slot_id
      )

      self._alt_parser_result_dict[alt_id] = parser_result
      self._alt_parser_dict[alt_id] = fetched_parser

      return parser_result

    except Exception as err:
      # print("#################### _ensure_parser_result FAILED! ####################")
      self.any_error = True
      logger.warning("Target [partial] AST does not respect the grammar!", exc_info=err)
      fetched_parser.dbg_print_tail_stack()
      err_dbg_info = fetched_parser._dbg_info_finish_for_ex_error()

      err_parser_result = self._parser_result_as_dict(
        False,  # is_acceptable
        False,  # is_done
        True,  # is_error
        err_dbg_info,  # dbg_info
        None  # stuck_slot_id
      )

      self._alt_parser_result_dict[alt_id] = err_parser_result
      raise err

  def _parser_result_as_dict(
    self,
    is_acceptable,
    is_done,
    is_error,
    dbg_info,
    stuck_slot_id
  ):
    return {
      "is_acceptable": is_acceptable,
      "is_done": is_done,
      "is_error": is_error,
      "dbg_info": dbg_info,
      "stuck_slot_id": stuck_slot_id,
    }


  def _update_alt_node_as_checkpoint(self, alt_id):
    alt_node = self._alt_tree_dict[alt_id]
    if alt_node["is_checkpoint"]: return
    parser = self._fetch_parser(alt_id)
    self._alt_parser_dict[alt_id] = parser
    alt_node["is_checkpoint"] = True
    # print(f"!!! Updating (alt_id:{alt_id}) as checkpoint.")

  def _fetch_parser(self, alt_id):
    """assume the parsing result of alt_id is already available. We don't care. Return a parser"""
    assert alt_id == 0 or alt_id in self._alt_parser_result_dict
    alt_node = self._alt_tree_dict[alt_id]

    # 1 exists in cache (@satbek)
    if alt_id in self._alt_parser_dict and self._alt_parser_dict[alt_id] is not None:
      if alt_node["is_checkpoint"]:
        # print("# _fetch_parser cloning from checkpoint:", alt_id)
        return self._alt_parser_dict[alt_id].clone()
      else:
        parser = self._alt_parser_dict[alt_id]
        self._alt_parser_dict[alt_id] = None
        return parser

    # 2 does not exist in cache (@satbek)
    assert not alt_node["is_checkpoint"]
    prev_id = alt_node["prev_alt_id"]
    assert prev_id is not None
    expansion = alt_node["expansion"]
    fetched_parser = self._fetch_parser(prev_id)
    is_accepted, _ = fetched_parser.add_expansion_parse_until_stuck(expansion)
    assert is_accepted
    assert fetched_parser.last_time_stuck_slot_id == self._alt_parser_result_dict[alt_id]["stuck_slot_id"]
    return fetched_parser

  def _get_alt_partial_ast(self, alt_node):
    alt_id = alt_node["alt_id"]
    assert alt_id in self._alt_parser_dict
    parser = self._alt_parser_dict[alt_id]
    elem_list = parser.get_current_elem_list()
    return d_ast_pretty.elem_list_to_mapanno_ast(elem_list)

  def _get_alt_debug_history(self, alt_node):
    # get dbg_debug_info from the chain of parents start from alt_node
    alt_debug_history = []
    while alt_node["alt_id"] != 0:
      alt_id = alt_node["alt_id"]
      dbg_info = self._alt_parser_result_dict[alt_id]["dbg_info"]
      range_cursor = self._slot_dict[alt_node["expansion"].corres_slot_id].range_cursor
      alt_step = alt_node["alt_step"]
      range_info = None
      if alt_step == 1:
        assert len(range_cursor[0]) == 1
      else:
        range_info = (range_cursor[0][1], range_cursor[1], range_cursor[2])
      alt_debug_history.append({
        "alt_step": alt_step,
        "range_info": range_info,
        "next_choices_status": alt_node["next_choices_status"] ,
        "dbg_info": dbg_info
      })
      alt_node = self._alt_tree_dict[alt_node["prev_alt_id"]]
    alt_debug_history = list(reversed(alt_debug_history))
    return alt_debug_history


  def _set_program_str(self, code_str):
    # parse the code, set self.expansion_programs
    # print(f"\n\n++++++++++++++++++++++++++++++++++++++++ _set_program_str. {len(code_str)} ++++++++++++++++++++++++++++++++++++++++\n")
    expansion_programs = d_grammar_rules.parse_analyze_rules_optim(code_str)
    self.expansion_programs = expansion_programs
    # print("++++++++++++  set self.expansion_programs")


# end of class `TransSession`

############################# utils #############################
def _is_elem_NT(visit_elem) -> bool:
  if not isinstance(visit_elem, list): return False
  if visit_elem[0] == "anno": return False
  assert visit_elem[0] != "fragment"
  assert isinstance(visit_elem[1], int)
  return True
