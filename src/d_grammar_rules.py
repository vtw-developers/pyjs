import re
from typing import List, Tuple

import d_consts
import d_utils


def parse_analyze_rules(code_str, show_disable=False) -> Tuple[List[dict], dict]:
  # No longer using the old preprocessing code. Otherwise offset is wrong.
  # code_str = "\n".join([x for x in code_str.split("\n") if not x.strip().startswith(";") and not x.strip() == ""])
  expected_rule_count = len(("\n" + code_str).split("\n(match_expand")) + len(("\n" + code_str).split("\n(ext_match_expand")) - 2
  sexpr_list, sexpr_loc_list, err = d_utils.parse_sexpr_list(code_str)
  assert expected_rule_count == len(sexpr_list)

  if sexpr_list is None:
    print("parsing error:", err)
    assert False, "parsing error"

  expansion_programs = []
  for sexpr in sexpr_list:
    decl_name = sexpr[0]
    if decl_name == "match_expand":
      assert len(sexpr) == 3, "match_expand expected length 3"
      expansion_programs.append({
        "type": "match_expand",
        "match": sexpr[1],
        "expand": sexpr[2]
      })
    elif decl_name == "ext_match_expand":
      assert len(sexpr) == 4, "ext_match_expand expected length 4"
      assert sexpr[3][0] == "flags", "ext_match_expand should have flags"
      flags = {x:True for x in sexpr[3][1:]}
      if '"disabled"' not in flags or show_disable:
        expansion_programs.append({
          "type": "ext_match_expand",
          "match": sexpr[1],
          "expand": sexpr[2],
          "flags": flags
        })
      else:
        if d_consts.DEBUG_VERBOSE > 0: print("# _set_program_str skipping disabled rule.")
    else:
      print("Unknown declarator name:", decl_name)
      assert False, "Unknown declarator name"

  def _get_rule_summary(rule):
    rule_type = rule["type"]

    def _get_main_symbols(match_or_expand):
      maex_type = match_or_expand[0]
      if maex_type == "fragment":
        return [str(x) for x in match_or_expand[1:]]

    if rule_type == "match_expand" or rule_type == "ext_match_expand":
      match_symbols = _get_main_symbols(rule["match"])
      expand_symbols = _get_main_symbols(rule["expand"])
      return f"{' '.join(match_symbols)} => {' '.join(expand_symbols)}"
    else:
      print("# Unsupported rule_type:", rule_type)
      assert False, "rule_type_not_supported"

  rule_ids = list(range(len(expansion_programs)))
  dbg_info = {
    "rule_ids": rule_ids,
    "summary_dict": {i:_get_rule_summary(expansion_programs[i]) for i in rule_ids},
    "rule_loc_dict": {i:sexpr_loc_list[i+1][0] for i in rule_ids}
  }

  return expansion_programs, dbg_info


def parse_analyze_rules_optim(
  trules_str: str,
  show_disable: bool = False
) -> List[dict]:
  '''
  Optimized version of parse_analyze_rules that only returns the parsed translation rules.
  '''
  # Preprocess to remove comments and blank lines
  trules_str = '\n'.join([
    x for x in trules_str.split('\n')
    if not (x.strip().startswith(';') or x.strip() == '')
  ])

  # Split the ruleset into individual rules for optimized parsing
  split_indices = [m.start() for m in re.finditer(r'\((?:match_expand|ext_match_expand)', trules_str)]
  trules_list = []
  for i, idx in enumerate(split_indices):
      end = split_indices[i+1] if i+1 < len(split_indices) else len(trules_str)
      trules_list.append(trules_str[idx:end])

  trules_parsed = []
  for trule in trules_list:
    sexpr_list, _, err = d_utils.parse_sexpr_list(trule)
    assert sexpr_list is not None, 'Translation rule parsing error: ' + str(err)
    assert len(sexpr_list) == 1, 'Each rule should parse to a single s-expression.'
    sexpr = sexpr_list[0]
    decl_name = sexpr[0]
    assert decl_name in ['match_expand', 'ext_match_expand'], f'Unknown declarator name: {decl_name}'
    if decl_name == 'match_expand':
      assert len(sexpr) == 3, 'match_expand expected length 3'
      trules_parsed.append({
        'type': 'match_expand',
        'match': sexpr[1],
        'expand': sexpr[2]
      })
    else:
      assert len(sexpr) == 4, 'ext_match_expand expected length 4'
      assert sexpr[3][0] == 'flags', 'ext_match_expand should have flags'
      flags = {x: True for x in sexpr[3][1:]}
      if '"disabled"' not in flags or show_disable:
        trules_parsed.append({
          'type': 'ext_match_expand',
          'match': sexpr[1],
          'expand': sexpr[2],
          'flags': flags
        })

  return trules_parsed


def pretty_s_expr(s_expr) -> str:
  '''
  `sExpr` has a very similar structure to DuoGlot style AST's.
  This function returns a string version of it which is THE version
  that is parsed by the DuoGlot transpiler.
  Refer to p_rule_inferencer.py for more information.
  '''
  if isinstance(s_expr, list):
    result = ['(']
    for i in range(0, len(s_expr)):
      result.append(pretty_s_expr(s_expr[i]))
      if i < len(s_expr) - 1:
        result.append(' ')
    result.append(')')
    return ''.join(result)
  else:
    return str(s_expr)


def pretty_rule(rule: dict) -> str:
  '''
  Pretty-prints a translation rule to the standard format.
  Refer to p_rule_inferencer.py for more information.
  PARAM rule - as parsed by parse_analyze_rules()
  '''
  rule_type = rule['type']
  match = rule['match']
  expand = rule['expand']
  assert rule_type == 'match_expand', 'sanity check'
  return \
    f'({rule_type}\n' \
    f'  {pretty_s_expr(match)}\n' \
    f'  {pretty_s_expr(expand)}\n)'


def pretty_s_expr_tree_like(s_expr, indent_size=2, global_indent='  ') -> str:
  def _rec(s_expr, indent_level, indent_size, global_indent):
    # terminal
    if isinstance(s_expr, str):
      return global_indent + (' ' * (indent_size * indent_level)) + s_expr
    # non-terminal with single terminal child
    if isinstance(s_expr, list) and len(s_expr) == 2 and isinstance(s_expr[0], str) and isinstance(s_expr[1], str):
      return global_indent + (' ' * (indent_size * indent_level)) + '(' + s_expr[0] + ' ' + s_expr[1] + ')'
    # nostr
    if isinstance(s_expr, list) and len(s_expr) == 1:
      return global_indent + (' ' * (indent_size * indent_level)) + '(' + s_expr[0] + ')'
    result = global_indent + (' ' * (indent_size * indent_level)) + '('
    result += s_expr[0]
    for i in range(1, len(s_expr)):
      result += '\n' + _rec(s_expr[i], indent_level+1, indent_size, global_indent)
    result += '\n' + global_indent + (' ' * (indent_size * indent_level)) + ')'
    return result
  result = _rec(s_expr, 0, indent_size, global_indent)
  return result
