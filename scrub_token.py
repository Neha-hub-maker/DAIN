"""
History rewrite script: removes hardcoded HF_TOKEN from test_hf.py.
Called by git filter-branch --tree-filter.
"""
import re
import pathlib

target = pathlib.Path("test_hf.py")
if not target.exists():
    exit(0)

text = target.read_text(encoding="utf-8")

# Remove any line that contains a hardcoded hf_ token
cleaned = re.sub(
    r'HF_TOKEN\s*=\s*["\']?\s*hf_[A-Za-z0-9_]+\s*["\']?',
    'HF_TOKEN = os.environ.get("HF_TOKEN", "")',
    text
)

target.write_text(cleaned, encoding="utf-8")
