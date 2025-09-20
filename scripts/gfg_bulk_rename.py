from pathlib import Path


CWD = Path(__file__).parent

gfg_fpaths = sorted(CWD.glob("GFG*.py"))
print(len(gfg_fpaths), "GFG files found")

for idx, fpath in enumerate(gfg_fpaths, start=1):
  print(fpath)
  parent = fpath.parent
  name = fpath.stem
  assert name.startswith("GFG_")

  # remove old prefix
  new_name = name[4:]
  new_prefix = f'G{idx:04d}_'
  new_fpath = parent / f"{new_prefix}{new_name}.py"

  print(new_fpath)

  # rename file
  fpath.rename(new_fpath)
