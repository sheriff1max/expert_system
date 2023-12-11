def calculate(left, operator, right, operator_and: str) -> float:
    """Вычисляет результат двух оперсандов и одного операнда: и|или"""
    if operator == operator_and:
        return min(left, right)
    else:
        return max(left, right)


def facts2nums(expr: list[str], facts: dict) -> list:
    """Заменяем известные факты на числа."""
    new_expr = []
    for sym in expr:
        if sym in facts:
            new_expr.append(facts[sym])
        else:
            new_expr.append(sym)
    return new_expr


def not2num(expr: list, operator_not: str) -> list:
    """Преобразование логического 'не' к числу."""
    new_expr = []
    flag_not = False

    for sym in expr:
        if sym == operator_not:
            flag_not = True
        elif flag_not:
            new_expr.append(-sym)
            flag_not = False
        else:
            new_expr.append(sym)
    return new_expr


def calculate_staples(expr: list, operator_and: str) -> list:
    """Вычисление результата первых-встреченных скобок."""
    new_expr = []
    start_idx = None

    i_left_staple = 0
    count_left_staples = expr.count('(')

    for idx, sym in enumerate(expr):

        if sym == '(':
            i_left_staple += 1
            start_idx = idx
        elif sym == ')':
            result_calculate = calculate(expr[start_idx+1], expr[start_idx+2], expr[idx-1], operator_and)
            new_expr.append(result_calculate)
            i_left_staple = 0
            continue

        if i_left_staple != count_left_staples or count_left_staples == 0:
            new_expr.append(sym)
    return new_expr


def calculate_confidence_two_rules(
        confidence1: float,
        confidence2: float,
) -> float:
    """Подсчёт коэф. уверенности двух правил."""
    if confidence1 == 1.0 or confidence2 == 1.0:
        return 1.0
    elif confidence1 == -1.0 or confidence2 == -1.0:
        return -1.0
    elif confidence1 * confidence2 <= 0:
        return confidence1 + confidence2
    elif confidence1 > 0 and confidence2 > 0:
        return confidence1 + confidence2 - confidence1 * confidence2
    elif confidence1 < 0 and confidence2 < 0:
        return confidence1 + confidence2 + confidence1 * confidence2
