from math_logic import Rule, api


OPERATOR_AND = '&'
OPERATOR_OR = '|'
OPERATOR_NOT = '-'
MATH_SYMS = [OPERATOR_AND, OPERATOR_OR, OPERATOR_NOT, '(', ')']


facts = {
    'A': 0.2,
    'B': 0.6,
    'C': -0.5,
}

rules = [
    Rule(
        name_rule='P1',
        confidence_coefficient_rule=0.6,
        formula=['A', OPERATOR_OR, OPERATOR_NOT, 'C'],
        result_fact_name='K',
    ),
    Rule(
        name_rule='P2',
        confidence_coefficient_rule=0.7,
        formula=['K', OPERATOR_AND, '(', 'B', OPERATOR_OR, 'A', ')'],
        result_fact_name='W',
    ),
]

# facts = {
#     'A': 0.8,
#     'B': 0.3,
#     'C': 0.5,
# }

# rules = [
#     Rule(
#         name_rule='P1',
#         confidence_coefficient_rule=0.6,
#         formula=['A'],
#         result_fact_name='Z',
#     ),
#     Rule(
#         name_rule='P2',
#         confidence_coefficient_rule=0.4,
#         formula=[OPERATOR_NOT, 'B', '&', '(', 'A', '|', 'C', ')'],
#         result_fact_name='Z',
#     ),
# ]

# facts = {
#     'F': 0.3,
#     'D': 0.7,
#     'A': -0.4,
#     'K': 0.6,
# }

# rules = [
#     Rule(
#         name_rule='P1',
#         confidence_coefficient_rule=0.4,
#         formula=['F', OPERATOR_AND, 'D'],
#         result_fact_name='R',
#     ),
#     Rule(
#         name_rule='P2',
#         confidence_coefficient_rule=0.8,
#         formula=[OPERATOR_NOT, 'A', OPERATOR_AND, 'K'],
#         result_fact_name='R',
#     ),
# ]

# facts = {
#     'A': 0.1,
#     'B': 0.7,
#     'C': -0.2,
# }

# rules = [
#     Rule(
#         name_rule='P1',
#         confidence_coefficient_rule=0.9,
#         formula=['A', OPERATOR_OR, '(', OPERATOR_NOT, 'B', OPERATOR_AND, 'C', ')'],
#         result_fact_name='D',
#     ),
#     Rule(
#         name_rule='P2',
#         confidence_coefficient_rule=0.5,
#         formula=['B', OPERATOR_AND, OPERATOR_NOT, 'C'],
#         result_fact_name='D',
#     ),
# ]


if __name__ == '__main__':

    result_facts, facts_result_steps = api(
        facts=facts,
        rules=rules,
        operator_and=OPERATOR_AND,
        operator_not=OPERATOR_NOT,
        math_syms=MATH_SYMS,
    )
    print(result_facts)
