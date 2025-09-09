# Environment setup
```bash
# conda env
conda create --name test_env "python>=3.12"
conda activate pirel_env

# dependencies
pip install -r requirements.txt

# install NodeJS with NVM https://github.com/nvm-sh/nvm
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
nvm install 21.5.0
```

# Running unit tests for files in `src`
```bash
# from src directory
python -m unittest p_visitor_py_test.py
```

# Running a memory profiler
```bash
# from https://github.com/bloomberg/memray
pip install memray

python -m memray run p_learn_apply_rules.py <conf-name>
memray flamegraph p_learn_apply_rules.<some-id>.bin
```
