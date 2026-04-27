import formulas

import formulas


def evaluate_formula_with_context(formula, context):
    """Evaluate an Excel-style formula against a context dict."""
    if not formula or not formula.strip():
        return None

    if not formula.strip().startswith("="):
        formula = "=" + formula

    _, ast = formulas.Parser().ast(formula)
    compiled = ast.compile()
    needed = set(compiled.inputs.keys())

    filtered = {
        k: v for k, v in context.items()
        if k in needed and v is not None
    }

    if not needed.issubset(filtered.keys()):
        return None

    return str(compiled(**filtered))