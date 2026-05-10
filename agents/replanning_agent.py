# ============================================
# File: agents/replanning_agent.py
# Description:
# Handles dynamic replanning whenever
# paths become blocked.
# ============================================


class ReplanningAgent:
    """
    Adaptive replanning system.
    """

    def __init__(
        self,
        environment,
        search_algorithms
    ):

        self.environment = environment

        self.search_algorithms = (
            search_algorithms
        )

    def is_path_blocked(
        self,
        path
    ):
        """
        Check whether path contains
        blocked roads or hazard zones.
        """

        for position in path:

            if (
                position
                in
                self.environment.blocked_roads
            ):

                return True

            if self.environment.is_hazard_position(
                position
            ):

                return True

        return False

    def generate_alternative_route(
        self,
        algorithm_name,
        start_position,
        goal_position
    ):
        """
        Generate alternative path.
        """

        selected_algorithm = self.search_algorithms.get(
            algorithm_name,
            self.search_algorithms["A*"]
        )

        new_path = (
            selected_algorithm.find_path(
                start_position,
                goal_position
            )
        )

        return new_path
