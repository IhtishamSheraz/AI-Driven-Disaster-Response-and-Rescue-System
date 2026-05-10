# ============================================
# File: analytics/confusion_matrix_generator.py
# Description:
# Generate confusion matrix visualization.
# ============================================

import matplotlib.pyplot as plt

from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay
)


class ConfusionMatrixGenerator:
    """
    Plot confusion matrices.
    """

    def display_confusion_matrix(
        self,
        y_test,
        predictions
    ):
        """
        Generate confusion matrix graph.
        """

        matrix = confusion_matrix(
            y_test,
            predictions
        )

        display = (
            ConfusionMatrixDisplay(
                confusion_matrix=matrix
            )
        )

        display.plot()

        plt.title(
            "Confusion Matrix"
        )

        plt.show()