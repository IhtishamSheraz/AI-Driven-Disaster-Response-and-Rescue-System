# ============================================
# File: machine_learning/data_preprocessor.py
# Description:
# Preprocess dataset for ML training.
# ============================================

from sklearn.model_selection import (
    train_test_split
)

from sklearn.preprocessing import (
    StandardScaler
)


class DataPreprocessor:
    """
    Prepare ML dataset.
    """

    def preprocess_dataset(
        self,
        dataframe
    ):
        """
        Split and normalize dataset.
        """

        features = dataframe.drop(
            "priority",
            axis=1
        )

        labels = dataframe["priority"]

        (
            x_train,
            x_test,
            y_train,
            y_test

        ) = train_test_split(

            features,

            labels,

            test_size=0.2,

            random_state=42
        )

        scaler = StandardScaler()

        x_train = scaler.fit_transform(
            x_train
        )

        x_test = scaler.transform(
            x_test
        )

        return (

            x_train,

            x_test,

            y_train,

            y_test
        )