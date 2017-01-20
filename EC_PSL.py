from problog.program import PrologString
from problog import get_evaluatable

model = """0.3::a.  query(a)."""
result = get_evaluatable().create_from(PrologString(model)).evaluate()
