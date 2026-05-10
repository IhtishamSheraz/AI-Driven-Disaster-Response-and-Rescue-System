# ============================================
# File: search_algorithms/astar_search.py
# Description:
# A* Search Algorithm Implementation
# ============================================


class AStarSearch:
    """
    A* pathfinding algorithm.
    """

    def __init__(
        self,
        environment
    ):
        """
        Initialize algorithm.
        """

        self.environment = environment

    def calculate_heuristic(
        self,
        current_position,
        goal_position
    ):
        """
        Calculate Manhattan distance heuristic.
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
        came_from,
        current_node
    ):
        """
        Reconstruct final path.
        """

        path = [

            current_node
        ]

        while current_node in came_from:

            current_node = (
                came_from[current_node]
            )

            path.append(
                current_node
            )

        path.reverse()

        return path

    def find_path(
        self,
        start_position,
        goal_position
    ):
        """
        Execute A* search algorithm.
        """

        # =====================================
        # OPEN + CLOSED SETS
        # =====================================

        open_set = []

        closed_set = set()

        # =====================================
        # PATH TRACKING
        # =====================================

        came_from = {}

        g_score = {}

        f_score = {}

        # =====================================
        # INITIALIZE START NODE
        # =====================================

        open_set.append(
            start_position
        )

        g_score[start_position] = 0

        f_score[start_position] = (
            self.calculate_heuristic(

                start_position,

                goal_position
            )
        )

        # =====================================
        # MAIN LOOP
        # =====================================

        while len(open_set) > 0:

            # =====================================
            # GET LOWEST F-SCORE NODE
            # =====================================

            current_node = min(

                open_set,

                key=lambda node:
                f_score.get(
                    node,
                    float("inf")
                )
            )

            # =====================================
            # GOAL REACHED
            # =====================================

            if current_node == goal_position:

                return self.reconstruct_path(

                    came_from,

                    current_node
                )

            open_set.remove(
                current_node
            )

            closed_set.add(
                current_node
            )

            # =====================================
            # GET VALID NEIGHBORS
            # =====================================

            neighbors = (
                self.environment.get_neighbors(
                    current_node
                )
            )

            for neighbor in neighbors:

                # =====================================
                # SKIP BLOCKED ROADS
                # =====================================

                if (
                    neighbor
                    in
                    self.environment.blocked_roads
                ):

                    continue

                # =====================================
                # SKIP CLOSED NODE
                # =====================================

                if neighbor in closed_set:

                    continue

                # =====================================
                # CALCULATE G SCORE
                # =====================================

                tentative_g_score = (

                    g_score[current_node]
                    +
                    1
                )

                # =====================================
                # ADD TO OPEN SET
                # =====================================

                if (
                    neighbor
                    not in open_set
                ):

                    open_set.append(
                        neighbor
                    )

                elif (
                    tentative_g_score
                    >=
                    g_score.get(
                        neighbor,
                        float("inf")
                    )
                ):

                    continue

                # =====================================
                # UPDATE BEST PATH
                # =====================================

                came_from[neighbor] = (
                    current_node
                )

                g_score[neighbor] = (
                    tentative_g_score
                )

                f_score[neighbor] = (

                    g_score[neighbor]

                    +

                    self.calculate_heuristic(

                        neighbor,

                        goal_position
                    )
                )

        # =====================================
        # NO PATH FOUND
        # =====================================

        return []