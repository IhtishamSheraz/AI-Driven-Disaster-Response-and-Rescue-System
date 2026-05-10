# ============================================
# File: evaluation/search_algorithm_comparator.py
# Description:
# Compare search algorithms using:
# - Path length
# - Runtime
# - Nodes explored
# ============================================

import time


class SearchAlgorithmComparator:
    """
    Compare search algorithm performance.
    """

    def compare_algorithms(
        self,
        algorithms,
        start_position,
        goal_position
    ):
        """
        Execute and compare algorithms.
        """

        comparison_results = []

        for algorithm_name, algorithm in algorithms.items():

            start_time = time.time()

            path = algorithm.find_path(
                start_position,
                goal_position
            )

            end_time = time.time()

            execution_time = (
                end_time - start_time
            )

            result = {

                "algorithm": algorithm_name,

                "path_length": len(path),

                "execution_time": execution_time,

                "path": path
            }

            comparison_results.append(result)

        return comparison_results