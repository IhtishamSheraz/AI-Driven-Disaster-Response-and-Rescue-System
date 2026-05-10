# ============================================
# File: machine_learning/knn_model.py
# Description:
# k-Nearest Neighbors ML model.
# ============================================


from sklearn.neighbors import (
    KNeighborsClassifier
)

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
    
)


class KNNModel:
    """
    kNN classifier model.
    """

    def __init__(self):

        self.model = (
            KNeighborsClassifier(
                n_neighbors=5
            )
        )

    def train_model(
        self,
        x_train,
        y_train
    ):
        """
        Train kNN model.
        """

        self.model.fit(
            x_train,
            y_train
        )
    def evaluate_model(
        self,
        x_test,
        y_test
    ):
        """
        Evaluate kNN model.
        """

        predictions = (
            self.model.predict(x_test)
        )

        metrics = {

            "accuracy":
            accuracy_score(
                y_test,
                predictions
            ),

            "precision":
            precision_score(
                y_test,
                predictions,
                average='weighted'
            ),

            "recall":
            recall_score(
                y_test,
                predictions,
                average='weighted'
            ),

            "f1_score":
            f1_score(
                y_test,
                predictions,
                average='weighted'
            ),

            "confusion_matrix":
            confusion_matrix(
                y_test,
                predictions
            )
        }

        return metrics
    
    def predict(
        self,
        features
    ):

        return self.model.predict(
            features
        )