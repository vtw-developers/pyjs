# Environment setup
```bash
# conda env
conda create --name pirel_env python=3.10.16
conda activate pirel_env

# dependencies
pip install -r requirements.txt
```

# Running unit tests for files in `src`
```bash
# from src directory
python -m unittest p_visitor_py_test.py
```
