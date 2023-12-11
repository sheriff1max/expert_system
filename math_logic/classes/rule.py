class Rule:
    """Класс правила."""

    def __init__(
            self,
            name_rule: str,
            confidence_coefficient_rule: float,
            formula: list[str],
            result_fact_name: str,
    ):
        # Название/id правила.
        self.name_rule = name_rule
        # Коэф. уверенности правила
        self.confidence_coefficient_rule = confidence_coefficient_rule
        # Формула правила.
        self.formula = formula
        # Название результирующего факта.
        self.result_fact_name = result_fact_name

        # Коэф. уверенности логического выражения.
        self.confidence_coefficient_formula = None
        # Коэф. уверенности результирующего факта
        self.confidence_coefficient_result_fact = None

        self.log_list = [formula]

    def forward(self, expr: list[str]) -> None:
        """"""
        self.confidence_coefficient_formula = expr
        if expr not in self.log_list:
            self.log_list.append(expr)

    def get_last_formula(self) -> list[str]:
        """"""
        if self.confidence_coefficient_formula:
            return self.confidence_coefficient_formula
        else:
            return self.formula

    def calculate_confidence_coefficient_result_fact(self) -> None:
        """"""
        self.confidence_coefficient_result_fact = self.confidence_coefficient_formula * self.confidence_coefficient_rule

    def get_log_list(self) -> list:
        return self.log_list

    def __repr__(self) -> str:
        return f'{self.name_rule}: {self.formula} -> {self.result_fact_name}'
