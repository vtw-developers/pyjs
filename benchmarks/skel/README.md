# SKEL benchmarks

Python programs included in this directory were obtained
from [SKEL's replication package](https://github.com/lty12b9b0a1/SKEL)

```sh
for d in SKEL/benchmarks_new/*
do
  python SKEL/scripts/normalize.py $d
  mv $d/source_normalized.py \
    PiREL/benchmarks/skel/$(basename $d).py
done
mv py_evtx_original.py evtx.py
cp -r SKEL/benchmarks_new/py_evtx_original/evtx_data \
  PiREL/benchmarks/skel/evtx.d
mkdir PiREL/benchmarks/skel/toml.d
cp SKEL/benchmarks_new/toml/example.toml \
  PiREL/benchmarks/skel/toml.d/example.toml
```

In `evtx.py`, the use of `six.string_types` got expanded to `str`
to remove the dependency on `six`.

In `strsim.py`, `"上海"` and `"上海市"` got substituted
with `"SH"` and `"SHC"`, respectively, as a work around for tree-sitter.

`SKEL/benchmarks_new/*/tracer_skip.py` modules were inlined
with adjusted paths to test inputs.

Functions consisting only of dead code were then eliminated.
