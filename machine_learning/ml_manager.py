# ============================================
# File: machine_learning/ml_manager.py
# Description:
# Main ML management system.
# ============================================

from machine_learning.dataset_generator import (
    DatasetGenerator
)

from machine_learning.data_preprocessor import (
    DataPreprocessor
)

from machine_learning.knn_model import (
    KNNModel
)

from machine_learning.naive_bayes_model import (
    NaiveBayesModel
)


class MachineLearningManager:
    """
    Main ML system manager.
    """

    def __init__(self):

        self.dataset_generator = (
            DatasetGenerator()
        )

        self.preprocessor = (
            DataPreprocessor()
        )

        self.knn_model = (
            KNNModel()
        )

        self.naive_bayes_model = (
            NaiveBayesModel()
        )

    def execute_ml_pipeline(self):
        """
        Execute full ML workflow.
        """

        dataframe = (
            self.dataset_generator
            .generate_dataset()
        )

        (
            x_train,
            x_test,
            y_train,
            y_test

        ) = self.preprocessor.preprocess_dataset(
            dataframe
        )

        self.knn_model.train_model(
            x_train,
            y_train
        )

        self.naive_bayes_model.train_model(
            x_train,
            y_train
        )

        knn_metrics = (
            self.knn_model.evaluate_model(
                x_test,
                y_test
            )
        )

        naive_bayes_metrics = (

            self.naive_bayes_model
            .evaluate_model(
                x_test,
                y_test
            )
        )
        self.knn_metrics = knn_metrics

        self.naive_bayes_metrics = naive_bayes_metrics
        print("\n====================================")
        print("      ML MODEL COMPARISON")
        print("====================================")

        print(
            "KNN Accuracy:",
            knn_metrics["accuracy"]
        )

        print(
            "Naive Bayes Accuracy:",
            naive_bayes_metrics["accuracy"]
        )

        print(
            "KNN Precision:",
            knn_metrics["precision"]
        )

        print(
            "Naive Bayes Precision:",
            naive_bayes_metrics["precision"]
        )

        print(
            "KNN Recall:",
            knn_metrics["recall"]
        )

        print(
            "Naive Bayes Recall:",
            naive_bayes_metrics["recall"]
        )

        print(
            "KNN F1 Score:",
            knn_metrics["f1_score"]
        )

        print(
            "Naive Bayes F1 Score:",
            naive_bayes_metrics["f1_score"]
        )
        print("\nKNN Confusion Matrix:")

        print(
            knn_metrics["confusion_matrix"]
        )

        print("\nNaive Bayes Confusion Matrix:")

        print(
            naive_bayes_metrics["confusion_matrix"]
        )
        print("\n====================================")

        if knn_metrics["accuracy"] > naive_bayes_metrics["accuracy"]:

            print("BEST MODEL SELECTED: KNN")

        else:

            print("BEST MODEL SELECTED: NAIVE BAYES")

        print("====================================\n")
        return (

            knn_metrics,

            naive_bayes_metrics
        )