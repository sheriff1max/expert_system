from .algo import (
    not2num,
    facts2nums,
    calculate,
    calculate_confidence_two_rules,
    calculate_staples,
    check_correct_count_staples,
    check_unknown_fact,
    check_correct_format_staples,
)
from .classes import Rule


def calculate_new_facts(
        facts: dict[str, float],
        rules: list[Rule],
        facts_result_steps: dict[str, list]
) -> list[dict[str, float], dict[str, list]]:
    """"""
    facts_copy = facts.copy()
    facts_result_steps_copy = facts_result_steps.copy()
    # Собираю правила одного и того же новога факта в один список.
    dict_rules_identical_facts = {}
    for rule in rules:
        result_fact_name = rule.result_fact_name
        if result_fact_name in dict_rules_identical_facts:
            dict_rules_identical_facts[result_fact_name].append(rule)
        else:
            dict_rules_identical_facts[result_fact_name] = [rule]

    # Удаляю факты, у которых ещё не все известны правила.
    valid_dict_rules_identical_facts = {}
    for fact, lst_rules in dict_rules_identical_facts.items():

        flag_good_rules = True
        for rule in lst_rules:
            if rule.confidence_coefficient_result_fact is None:
                flag_good_rules = False
                break

        if flag_good_rules:
            valid_dict_rules_identical_facts[fact] = lst_rules

    # Подсчитываю итоговый КУ
    for fact, lst_rules in valid_dict_rules_identical_facts.items():

        steps = []
        rule_names = []

        if len(lst_rules) == 1:
            confidence_coefficient = lst_rules[0].confidence_coefficient_result_fact
            steps.append(confidence_coefficient)
            rule_names.append(lst_rules[0].name_rule)
        else:
            confidence_coefficient = calculate_confidence_two_rules(
                lst_rules[0].confidence_coefficient_result_fact,
                lst_rules[1].confidence_coefficient_result_fact,
            )
            steps.append(lst_rules[0].confidence_coefficient_result_fact)
            steps.append(lst_rules[1].confidence_coefficient_result_fact)
            rule_names.append(lst_rules[0].name_rule)
            rule_names.append(lst_rules[1].name_rule)

        for i in range(2, len(lst_rules)):
            steps.append(confidence_coefficient)
            steps.append(lst_rules[i].confidence_coefficient_result_fact)
            rule_names.append(lst_rules[i].name_rule)
            confidence_coefficient = calculate_confidence_two_rules(
                confidence_coefficient,
                lst_rules[i].confidence_coefficient_result_fact,
            )

        facts_copy[fact] = confidence_coefficient
        facts_result_steps_copy[fact] = [steps, rule_names]
    return facts_copy, facts_result_steps_copy


def api(
    facts: dict[str, float],
    rules: list[Rule],
    operator_and: str,
    operator_not: str,
    math_syms: list[str],
) -> dict[str, float]:
    """Подсчёт коэф. уверенности Шортлиффа, основываясь
    на фактах и правилах."""
    updated_facts = facts.copy()
    facts_result_steps = {}

    flag_run = True
    while flag_run:
        flag_run = False

        for rule in rules:
            expr = rule.get_last_formula()

            if isinstance(expr, float):
                continue

            # Проверка на правильно написания формул.
            assert check_correct_count_staples(expr) is True
            assert check_correct_format_staples(expr, operator_not) is True

            # Проверка на неизвестность фактов в текущий момент.
            current_check_unknown_fact = check_unknown_fact(expr, math_syms, updated_facts)
            if current_check_unknown_fact:
                flag_run = True

            # Заменяем известные факты коэф. уверенностями.
            expr = facts2nums(expr, updated_facts)
            rule.forward(expr)

            # Обрабатываем операнд 'не'.
            expr = not2num(expr, operator_not)
            rule.forward(expr)

            # Вычисляем внутринность всех скобок.
            for _ in range(expr.count('(')):
                expr = calculate_staples(expr, operator_and)
                rule.forward(expr)

            while current_check_unknown_fact is False and len(expr) > 3:
                value = calculate(expr[0], expr[1], expr[2], operator_and)
                expr = [value, *expr[3:]]

            # Если в данном правиле известны все факты и все выражения упрощены
            # то считаем коэф. уверенности искомого факта.
            if current_check_unknown_fact is False and (len(expr) == 3 or len(expr) == 1):
                if len(expr) == 3:
                    expr = calculate(expr[0], expr[1], expr[2], operator_and)

                elif len(expr) == 1:
                    expr = expr[0]

                rule.forward(expr)
                rule.calculate_confidence_coefficient_result_fact()

                # Добавляем новые факты при всех его найденных правил.
                updated_facts, facts_result_steps = calculate_new_facts(updated_facts, rules, facts_result_steps)

    return updated_facts, facts_result_steps
