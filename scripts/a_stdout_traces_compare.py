'''
quick script to compare the execution traces of the source and target programs.
'''


import p_rule_applicator
import p_code_runner
import p_utils


src_stdout = p_utils.read_tmp_text('asrc.out')
tar_stdout = p_utils.read_tmp_text('atar.out')

src_trace = p_code_runner._extract_trace_from_stdout(src_stdout)
tar_trace = p_code_runner._extract_trace_from_stdout(tar_stdout)

are_traces_identical = p_rule_applicator.are_traces_equal_rec(src_trace, tar_trace)
print(f'src_trace == tar_trace: {are_traces_identical}')
