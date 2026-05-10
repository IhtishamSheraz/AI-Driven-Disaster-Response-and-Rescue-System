# ============================================
# File: search_algorithms/dfs_search.py
# Description:
# Depth First Search Algorithm
# ============================================


class DepthFirstSearch:
    """
    Depth First Search pathfinding.
    """

    def __init__(
        self,
        environment
    ):
        """
        Initialize DFS.
        """

        self.environment = environment

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
        Execute DFS search.
        """

        stack = [

            start_position
        ]

        visited = set()

        parent_map = {

            start_position: None
        }

        while len(stack) > 0:

            current_position = (
                stack.pop()
            )

            if (
                current_position
                in
                visited
            ):

                continue

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

            for neighbor in neighbors:

                if neighbor not in visited:

                    parent_map[neighbor] = (
                        current_position
                    )

                    stack.append(
                        neighbor
                    )

        return []