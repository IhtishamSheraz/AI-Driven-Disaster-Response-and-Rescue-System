# ============================================
# File: csp/mrv_heuristic.py
# Description:
# Implements Minimum Remaining Values
# heuristic for CSP optimization.
# ============================================


class MinimumRemainingValues:
    """
    MRV heuristic implementation.
    """

    @staticmethod
    def sort_victims_by_priority(victims):
        """
        Sort victims according to
        severity priority.
        """

        return sorted(
            victims,
            key=lambda victim:
            victim.get_priority_score(),
            reverse=True
        )

    @staticmethod
    def select_unassigned_variable(
        variables,
        domains,
        assignment,
        degree_map
    ):
        """
        MRV first, Degree Heuristic as tie-breaker.
        """

        unassigned_variables = [

            variable

            for variable
            in variables

            if variable not in assignment
        ]

        return min(

            unassigned_variables,

            key=lambda variable: (
                len(domains[variable]),
                -degree_map.get(variable, 0)
            )
        )
