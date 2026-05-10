# ============================================
# File: search_algorithms/bfs_search.py
# Description:
# Breadth First Search Algorithm
# ============================================

from collections import deque


class BreadthFirstSearch:
    """
    Breadth First Search pathfinding.
    """

    def __init__(
        self,
        environment
    ):
        """
        Initialize BFS.
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
        Execute BFS search.
        """

        queue = deque()

        queue.append(
            start_position
        )

        visited = set()

        visited.add(
            start_position
        )

        parent_map = {

            start_position: None
        }

        while len(queue) > 0:

            current_position = (
                queue.popleft()
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
            # USE VALID NEIGHBORS
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

                    queue.append(
                        neighbor
                    )

        return []