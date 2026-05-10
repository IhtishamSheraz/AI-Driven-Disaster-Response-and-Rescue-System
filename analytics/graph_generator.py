# ============================================
# File: analytics/graph_generator.py
# Description:
# Generate KPI graphs and save them.
# ============================================

import os

import matplotlib.pyplot as plt


class GraphGenerator:
    """
    Generate analytics graphs.
    """

    def __init__(self):

        self.output_folder = (
            "generated_reports"
        )

        if not os.path.exists(
            self.output_folder
        ):

            os.makedirs(
                self.output_folder
            )

    def generate_algorithm_comparison_chart(
        self,
        algorithm_results
    ):
        """
        Generate search comparison graph.
        """

        algorithm_names = []

        path_lengths = []

        for result in algorithm_results:

            algorithm_names.append(
                result["algorithm"]
            )

            path_lengths.append(
                result["path_length"]
            )

        plt.figure(figsize=(10, 5))

        plt.bar(
            algorithm_names,
            path_lengths
        )

        plt.title(
            "Search Algorithm Comparison"
        )

        plt.xlabel(
            "Algorithms"
        )

        plt.ylabel(
            "Path Length"
        )

        plt.tight_layout()

        save_path = (
            f"{self.output_folder}/"
            f"algorithm_comparison.png"
        )

        plt.savefig(save_path)

        plt.close()

        print(
            f"\nGraph saved at: "
            f"{save_path}"
        )

    def generate_ml_accuracy_chart(
        self,
        knn_accuracy,
        naive_bayes_accuracy
    ):
        """
        Generate ML accuracy graph.
        """

        model_names = [
            "kNN",
            "Naive Bayes"
        ]

        accuracy_values = [
            knn_accuracy,
            naive_bayes_accuracy
        ]

        plt.figure(figsize=(8, 5))

        plt.bar(
            model_names,
            accuracy_values
        )

        plt.title(
            "ML Accuracy Comparison"
        )

        plt.ylabel(
            "Accuracy"
        )

        plt.tight_layout()

        save_path = (
            f"{self.output_folder}/"
            f"ml_accuracy.png"
        )

        plt.savefig(save_path)

        plt.close()

        print(
            f"\nGraph saved at: "
            f"{save_path}"
        )