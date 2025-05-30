class TruthTableProcessor:
    def __init__(self, truth_table, variables):
        self.truth_table = truth_table
        self.variables = variables

    def get_normal_forms(self):
        sknf_terms = []
        sdnf_terms = []
        sknf_indices = []
        sdnf_indices = []

        for index, (values, _, result) in enumerate(self.truth_table):
            term = []
            if result:  # Если результат 1, добавляем в СДНФ
                sdnf_indices.append(index)
                for var in self.variables:
                    term.append(var if values[var] else f"!{var}")
                sdnf_terms.append(f"({' & '.join(term)})")
            else:  # Если результат 0, добавляем в СКНФ
                sknf_indices.append(index)
                for var in self.variables:
                    term.append(f"!{var}" if values[var] else var)
                sknf_terms.append(f"({' | '.join(term)})")

        return {
            "СКНФ": " & ".join(sknf_terms) if sknf_terms else "False",
            "СДНФ": " | ".join(sdnf_terms) if sdnf_terms else "True",
            "СКНФ Индексы": sknf_indices,
            "СДНФ Индексы": sdnf_indices
        }
