import os
from typing import List, Tuple

import p_consts
import p_utils
import p_visitor as pv
import p_visitor_py as pvpy


logger = p_utils.setup_logger(__name__)


class ReturnStatementSplitter(pv.Visitor):
  def __init__(self) -> None:
    super().__init__()
    self.counter = 1

  def pp_ret_stat(self, node: pvpy.ReturnStatementNode) -> str:
    pp = pvpy.PrettyPrinter(indent_with='    ')
    pp.visit(node)
    ppstr = '\n'.join(pp.lines)
    return ppstr

  def split_ret_stat(
    self,
    node: pvpy.ReturnStatementNode,
    ret_val_node: pv.AbstractNode
  ) -> bool:
    expr_stat_node = pvpy.ExpressionStatementNode('expression_statement')

    assign_node = pvpy.AssignmentNode('assignment')
    expr_stat_node.add_child(assign_node)
    assign_node.set_parent(expr_stat_node)

    temp_id_a = pvpy.IdentifierNode.build(f'retval_{self.counter}')
    temp_id_r = pvpy.IdentifierNode.build(f'retval_{self.counter}')
    self.counter += 1
    assign_node.add_child(temp_id_a)
    temp_id_a.set_parent(assign_node)
    assign_node.left = temp_id_a

    assign_node.add_child(ret_val_node)
    ret_val_node.set_parent(assign_node)
    assign_node.right = ret_val_node

    assert len(node.children) == 2
    node.children[1] = temp_id_r
    temp_id_r.set_parent(node)

    node_idx = node.parent.children.index(node)
    node.parent.children.insert(node_idx, expr_stat_node)
    expr_stat_node.set_parent(node.parent)

  def split_ret_stat_expr_list(
    self,
    node: pvpy.ReturnStatementNode,
    ret_val_node: pvpy.ExpressionListNode
  ) -> bool:
    # create a tuple from expression list
    tuple_node = pvpy.TupleNode('tuple')

    left_paren = pv.TerminalNode('(')
    tuple_node.add_child(left_paren)
    left_paren.set_parent(tuple_node)

    expr0 = ret_val_node.children[0]
    tuple_node.add_child(expr0)
    expr0.set_parent(tuple_node)

    for expr in ret_val_node.children[1:]:
      comma = pv.TerminalNode(',')
      tuple_node.add_child(comma)
      comma.set_parent(tuple_node)

      tuple_node.add_child(expr)
      expr.set_parent(tuple_node)

    right_paren = pv.TerminalNode(')')
    tuple_node.add_child(right_paren)
    right_paren.set_parent(tuple_node)

    return self.split_ret_stat(node, tuple_node)

  # VISIT METHODS
  def visit_ReturnStatementNode(self, node: pvpy.ReturnStatementNode) -> None:
    '''
    Split return statements with multiple return values into multiple return statements.
    '''
    if len(node.children) == 1:
      only_child = node.children[0]
      assert isinstance(only_child, pv.TerminalNode)
      assert only_child.node_type == 'return'
      logger.debug(f'excluded since it is an empty return statement: "{self.pp_ret_stat(node)}"')
      return

    assert len(node.children) == 2, f'Unexpected number of children in return statement: {len(node.children)}'
    ret_val_node = node.children[1]

    _SIMPLE_RETURN_TYPES = (
      pvpy.IdentifierNode,
      pvpy.FalseNode,
      pvpy.TrueNode,
      pvpy.IntegerNode,
      pvpy.StringNode,
    )
    if isinstance(ret_val_node, _SIMPLE_RETURN_TYPES ):
      logger.debug(f'excluded simple return value node: "{self.pp_ret_stat(node)}"')
      return

    _COMPLEX_RETURN_TYPES = (
      pvpy.UnaryOperatorNode,
      pvpy.NotOperatorNode,
      pvpy.BinaryOperatorNode,
      pvpy.CallNode,
      pvpy.SubscriptNode,
      pvpy.ConditionalExpressionNode,
      pvpy.ParenthesizedExpressionNode,
      pvpy.BooleanOperatorNode,
      pvpy.ComparisonOperatorNode,
      pvpy.AttributeNode,
      pvpy.TupleNode,
    )

    if isinstance(ret_val_node, _COMPLEX_RETURN_TYPES):
      logger.debug(f'split complex return value node: "{self.pp_ret_stat(node)}"')
      self.split_ret_stat(node, ret_val_node)
      return

    if isinstance(ret_val_node, pvpy.ExpressionListNode):
      logger.debug(f'split expression list return value node: "{self.pp_ret_stat(node)}"')
      self.split_ret_stat_expr_list(node, ret_val_node)
      return

    raise ValueError(f'Unexpected return value node type: {type(ret_val_node)}')

  @classmethod
  def split_return_stats(cls, main_code: str) -> str:
    src_parser = p_consts.PARSER_DICT['py']
    ts_tree = src_parser.parse(bytes(main_code, 'utf-8'))
    tree = pvpy.Tree.from_ts_tree(ts_tree)
    splitter = cls()
    splitter.visit(tree.root_node)
    pp = pvpy.PrettyPrinter(indent_with='    ')
    return pp.visit(tree.root_node)


SUBJECT_NAMES = ['G0014', 'G0016', 'G0017', 'G0020', 'G0021', 'G0022', 'G0028', 'G0029', 'G0030', 'G0042', 'G0045', 'G0046', 'G0051', 'G0052', 'G0053', 'G0054', 'G0056', 'G0059', 'G0060', 'G0065', 'G0067', 'G0068', 'G0071', 'G0073', 'G0076', 'G0078', 'G0079', 'G0080', 'G0081', 'G0082', 'G0083', 'G0084', 'G0085', 'G0087', 'G0089', 'G0092', 'G0096', 'G0097', 'G0099', 'G0105', 'G0107', 'G0110', 'G0111', 'G0113', 'G0115', 'G0116', 'G0119', 'G0131', 'G0132', 'G0139', 'G0140', 'G0142', 'G0143', 'G0144', 'G0145', 'G0146', 'G0148', 'G0151', 'G0152', 'G0153', 'G0155', 'G0156', 'G0157', 'G0159', 'G0160', 'G0161', 'G0162', 'G0166', 'G0167', 'G0168', 'G0169', 'G0173', 'G0174', 'G0176', 'G0177', 'G0178', 'G0179', 'G0180', 'G0181', 'G0182', 'G0184', 'G0185', 'G0186', 'G0191', 'G0192', 'G0196', 'G0200', 'G0204', 'G0207', 'G0212', 'G0215', 'G0216', 'G0217', 'G0219', 'G0221', 'G0223', 'G0225', 'G0229', 'G0232', 'G0234', 'G0236', 'G0239', 'G0241', 'G0245', 'G0247', 'G0249', 'G0250', 'G0251', 'G0255', 'G0256', 'G0257', 'G0258', 'G0264', 'G0268', 'G0273', 'G0277', 'G0278', 'G0283', 'G0286', 'G0287', 'G0289', 'G0290', 'G0294', 'G0296', 'G0297', 'G0299', 'G0301', 'G0302', 'G0306', 'G0314', 'G0315', 'G0316', 'G0317', 'G0322', 'G0323', 'G0324', 'G0325', 'G0326', 'G0330', 'G0331', 'G0334', 'G0335', 'G0336', 'G0337', 'G0339', 'G0340', 'G0343', 'G0344', 'G0345', 'G0349', 'G0350', 'G0351', 'G0353', 'G0354', 'G0357', 'G0359', 'G0360', 'G0362', 'G0366', 'G0371', 'G0372', 'G0373', 'G0381', 'G0383', 'G0386', 'G0387', 'G0389', 'G0390', 'G0392', 'G0394', 'G0396', 'G0399', 'G0400', 'G0402', 'G0404', 'G0405', 'G0406', 'G0409', 'G0410', 'G0415', 'G0417', 'G0420', 'G0424', 'G0426', 'G0428', 'G0432', 'G0437', 'G0439', 'G0441', 'G0442', 'G0444', 'G0445', 'G0447', 'G0448', 'G0451', 'G0454', 'G0456', 'G0457', 'G0458', 'G0460', 'G0464', 'G0465', 'G0468', 'G0472', 'G0481', 'G0484', 'G0486', 'G0492', 'G0494', 'G0497', 'G0499', 'G0500', 'G0501', 'G0504', 'G0505', 'G0510', 'G0511', 'G0514', 'G0515', 'G0524', 'G0526', 'G0528', 'G0529', 'G0530', 'G0532', 'G0534', 'G0536', 'G0543', 'G0548', 'G0549', 'G0551', 'G0552', 'G0553', 'G0556', 'G0561', 'G0566', 'G0568', 'G0574', 'G0575', 'G0578', 'G0579', 'G0582', 'G0584', 'G0586', 'G0587', 'G0591', 'G0592', 'G0593', 'G0594', 'G0598', 'G0601', 'G0602', 'G0603', 'G0604', 'G0608', 'G0610', 'G0612', 'G0615', 'G0617', 'G0619', 'G0620', 'G0623', 'G0626', 'G0628', 'G0630', 'G0631', 'G0635', 'G0637', 'G0638', 'G0639', 'G0640', 'G0643', 'G0644', 'G0647', 'G0649', 'G0655', 'G0656', 'G0664', 'G0669', 'G0670', 'G0672', 'G0675', 'G0676', 'G0677', 'G0678', 'G0679', 'G0680', 'G0681', 'G0687', 'G0688', 'G0689', 'G0690', 'G0691', 'G0693', 'G0694', 'G0699']

fpaths = sorted(p_consts.GFG_BENCHMARK_DIR.glob("G*.py"))
for fidx, fpath in enumerate(fpaths, start=1):

  subject_name = fpath.stem[:5]
  if subject_name not in SUBJECT_NAMES:
    continue

  code = p_utils.read_text(fpath)
  test, main, call = code.split(p_consts.TEST_MAIN_CALL_DELIMITER)

  res_str = ReturnStatementSplitter.split_return_stats(main)
  logger.debug(f'before: \n{main}\n')
  logger.debug(f'after: \n{res_str}\n')

  new_code = p_consts.TEST_MAIN_CALL_DELIMITER.join([
      test,
      f'\n{res_str}\n',
      call
  ])

  p_utils.write_text(fpath, new_code)
  logger.info(f'[{fidx}/{len(fpaths)}] Wrote to {fpath}')
