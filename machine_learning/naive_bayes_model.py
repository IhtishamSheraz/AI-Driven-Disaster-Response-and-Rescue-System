from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import (

    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


class NaiveBayesModel:

    def __init__(self):

        self.model = GaussianNB()

    def train_model(
        self,
        x_train,
        y_train
    ):

        self.model.fit(
            x_train,
            y_train
        )

    def evaluate_model(
        self,
        x_test,
        y_test
    ):

        predictions = self.model.predict(
            x_test
        )

        print("\nNAIVE BAYES RESULTS")

        print(
            "Accuracy:",
            accuracy_score(
                y_test,
                predictions
            )
        )

        print(
            "Precision:",
            precision_score(
                y_test,
                predictions,
                average='weighted'
            )
        )

        print(
            "Recall:",
            recall_score(
                y_test,
                predictions,
                average='weighted'
            )
        )

        print(
            "F1 Score:",
            f1_score(
                y_test,
                predictions,
                average='weighted'
            )
        )

        print(
            "Confusion Matrix:"
        )

        print(
            confusion_matrix(
                y_test,
                predictions
            )
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