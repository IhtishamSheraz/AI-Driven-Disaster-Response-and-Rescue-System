import pandas as pd

import random


class DatasetGenerator:

    def generate_dataset(self):

        dataframe = pd.read_csv(
            "datasets/global_disaster_response_2018_2024.csv"
        )

        dataframe = dataframe.dropna()

        # ======================================
        # CREATE NUMERIC SEVERITY
        # ======================================

        severity_map = {

            "Low": 1,
            "Moderate": 2,
            "High": 3,
            "Critical": 4
        }

        if "Severity" in dataframe.columns:

            dataframe["severity_encoded"] = (
                dataframe["Severity"]
                .map(severity_map)
                .fillna(1)
            )

        else:

            dataframe["severity_encoded"] = 1

        # ======================================
        # CREATE RESPONSE PRIORITY
        # ======================================

        import random

        priority_list = []

        for _, row in dataframe.iterrows():

            severity = row["severity_encoded"]

            if severity >= 4:

                priority = random.choice([3, 2])

            elif severity >= 3:

                priority = random.choice([2, 1])

            else:

                priority = random.choice([1, 2])

            priority_list.append(priority)

        dataframe["priority"] = priority_list

        if "distance" not in dataframe.columns:

            dataframe["distance"] = [
                random.randint(1, 50)
                for _ in range(len(dataframe))
            ]

        if "hazard_level" not in dataframe.columns:

            dataframe["hazard_level"] = [
                random.randint(1, 10)
                for _ in range(len(dataframe))
            ]

        if "medical_delay" not in dataframe.columns:

            dataframe["medical_delay"] = [
                random.randint(1, 12)
                for _ in range(len(dataframe))
            ]

       

        dataset = dataframe[[

            "severity_encoded",

            "distance",

            "hazard_level",

            "medical_delay",

            "priority"
]]
        return dataset