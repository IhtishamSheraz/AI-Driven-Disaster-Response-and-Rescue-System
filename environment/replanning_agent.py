# ============================================
# File: agents/replanning_agent.py
# Description:
# Responsible for:
# - detecting route failures
# - triggering replanning
# - selecting alternative paths
# ============================================


class ReplanningAgent:
    """
    Dynamic replanning engine.
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

    def is_path_blocked(self, path):
        """
        Check whether path contains
        blocked roads.
        """

        for position in path:

            if (
                position
                in
                self.environment.blocked_roads
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
        Recalculate route after blockage.
        """

        algorithm = (
            self.search_algorithms[
                algorithm_name
            ]
        )

        new_path = algorithm.find_path(
            start_position,
            goal_position
        )

        return new_path