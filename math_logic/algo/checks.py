def check_unknown_fact(
        expr: list,
        math_syms: list[str],
        facts: dict[str, float],
) -> bool:
    """Проверка на наличие неизвестных фактов."""
    for sym in expr:
        if isinstance(sym, str):
            if sym not in math_syms and sym not in facts:
                return True
    return False


def check_correct_count_staples(expr: list) -> bool:
    """Проверка на корректность кол-ва скобок."""
    if expr.count('(') == expr.count(')'):
        return True
    else:
        return False


def check_correct_format_staples(expr: list, operator_not: str) -> bool:
    """Проверка правильности формата скобок."""
    new_expr = [i for i in expr if i != operator_not]
    for i, sym in enumerate(new_expr):
        if sym == '(':
            if new_expr[i + 4] != ')':
                return False
    return True
