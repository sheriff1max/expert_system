def parse_input_formula(user_input_formula: str) -> list[str]:
    """Парсинг экспертного ввода формулы.

    Идеальный вид пользовательского ввода:
        сильный_ветер & (вчера_был_дождь | передавали_прогноз_дождя) """

    expr = []
    for token in user_input_formula.split():
        if len(token) > 1:
            if '(-' in token:
                expr.append('(')
                expr.append('-')
                expr.append(token[2:])
            elif ')' in token and '-' in token:
                expr.append('-')
                expr.append(token[1:-1])
                expr.append(')')
            elif '(' in token:
                expr.append('(')
                expr.append(token[1:])
            elif ')' in token:
                expr.append(token[:-1])
                expr.append(')')
            elif '-' in token:
                expr.append('-')
                expr.append(token[1:])
            else:
                expr.append(token)
        else:
            expr.append(token)
    print(expr)
    return expr
