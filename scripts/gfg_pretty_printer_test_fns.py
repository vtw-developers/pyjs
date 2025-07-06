template = '''
  def test_{subject_name}(self):
    gold_code, tree = self.load_test_subject('{subject_name}')
    pp_code = self.pp.visit(tree.root_node).strip()
    self.assertEqual(pp_code, gold_code)
'''.strip('\n')

with open('out.py', 'w') as fout:
  for i in range(1, 699 + 1):
    subject_name = f'G{i:04}'
    fout.write(template.format(subject_name=subject_name) + '\n\n')
