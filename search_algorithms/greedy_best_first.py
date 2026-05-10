# ============================================
# File: search_algorithms/greedy_best_first.py
# Description:
# Greedy Best First Search
# ============================================


class GreedyBestFirstSearch:
    """
    Greedy Best First Search pathfinding.
    """

    def __init__(
        self,
        environment
    ):
        """
        Initialize algorithm.
        """

        self.environment = environment

    def heuristic(
        self,
        current_position,
        goal_position
    ):
        """
        Manhattan distance heuristic.
        """

        return (

            abs(
                current_position[0]
                -
                goal_position[0]
            )

            +

            abs(
                current_position[1]
                -
                goal_position[1]
            )
        )

    def reconstruct_path(
        self,
        parent_map,
        goal_position
    ):
        """
        Reconstruct final path.
        """

        path = []

        current_position = goal_position

        while current_position is not None:

            path.append(
                current_position
            )

            current_position = (
                parent_map[current_position]
            )

        path.reverse()

        return path

    def find_path(
        self,
        start_position,
        goal_position
    ):
        """
        Execute Greedy Best First Search.
        """

        open_list = [

            start_position
        ]

        visited = set()

        parent_map = {

            start_position: None
        }

        while len(open_list) > 0:

            current_position = min(

                open_list,

                key=lambda position:
                self.heuristic(
                    position,
                    goal_position
                )
            )

            open_list.remove(
                current_position
            )

            # =====================================
            # GOAL REACHED
            # =====================================

            if (
                current_position
                ==
                goal_position
            ):

                return self.reconstruct_path(

                    parent_map,

                    goal_position
                )

            visited.add(
                current_position
            )

            # =====================================
            # USE ENVIRONMENT NEIGHBORS
            # =====================================

            neighbors = (
                self.environment.get_neighbors(
                    current_position
                )
            )

            for neighbor in neighbors:

                if neighbor not in visited:

                    visited.add(
                        neighbor
                    )

                    parent_map[neighbor] = (
                        current_position
                    )

                    open_list.append(
                        neighbor
                    )

        return []