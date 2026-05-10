# ============================================
# File: search_algorithms/hill_climbing.py
# Description:
# Hill Climbing Search Algorithm
# ============================================


class HillClimbingSearch:
    """
    Hill Climbing pathfinding.
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
        Execute Hill Climbing search.
        """

        current_position = start_position

        visited = set()

        parent_map = {

            start_position: None
        }

        while True:

            visited.add(
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

            # =====================================
            # USE ENVIRONMENT NEIGHBORS
            # =====================================

            neighbors = (

                self.environment.get_neighbors(
                    current_position
                )
            )

            # Remove visited
            neighbors = [

                neighbor

                for neighbor
                in neighbors

                if neighbor not in visited
            ]

            if len(neighbors) == 0:

                return []

            best_neighbor = min(

                neighbors,

                key=lambda position:
                self.heuristic(
                    position,
                    goal_position
                )
            )

            # =====================================
            # CHECK IF IMPROVING
            # =====================================

            current_heuristic = (
                self.heuristic(
                    current_position,
                    goal_position
                )
            )

            best_heuristic = (
                self.heuristic(
                    best_neighbor,
                    goal_position
                )
            )

            if (
                best_heuristic
                >=
                current_heuristic
            ):

                return []

            parent_map[best_neighbor] = (
                current_position
            )

            current_position = (
                best_neighbor
            )