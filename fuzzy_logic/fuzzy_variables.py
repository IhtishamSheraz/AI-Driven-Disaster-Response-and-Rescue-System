# ============================================
# File: fuzzy_logic/fuzzy_variables.py
# Description:
# Defines fuzzy input and output variables.
# ============================================

import numpy as np

import skfuzzy as fuzz

from skfuzzy import control as ctrl


class FuzzyVariables:
    """
    Define fuzzy variables.
    """

    def create_fuzzy_variables(self):
        """
        Create fuzzy inputs and outputs.
        """

        severity = ctrl.Antecedent(
            np.arange(0, 11, 1),
            "severity"
        )

        hazard = ctrl.Antecedent(
            np.arange(0, 11, 1),
            "hazard"
        )

        distance = ctrl.Antecedent(
            np.arange(0, 21, 1),
            "distance"
        )

        rescue_risk = ctrl.Consequent(
            np.arange(0, 101, 1),
            "rescue_risk"
        )

        severity["low"] = fuzz.trimf(
            severity.universe,
            [0, 0, 5]
        )

        severity["medium"] = fuzz.trimf(
            severity.universe,
            [3, 5, 7]
        )

        severity["high"] = fuzz.trimf(
            severity.universe,
            [6, 10, 10]
        )

        hazard["low"] = fuzz.trimf(
            hazard.universe,
            [0, 0, 5]
        )

        hazard["medium"] = fuzz.trimf(
            hazard.universe,
            [3, 5, 7]
        )

        hazard["high"] = fuzz.trimf(
            hazard.universe,
            [6, 10, 10]
        )

        distance["near"] = fuzz.trimf(
            distance.universe,
            [0, 0, 10]
        )

        distance["medium"] = fuzz.trimf(
            distance.universe,
            [5, 10, 15]
        )

        distance["far"] = fuzz.trimf(
            distance.universe,
            [10, 20, 20]
        )

        rescue_risk["low"] = fuzz.trimf(
            rescue_risk.universe,
            [0, 0, 40]
        )

        rescue_risk["medium"] = fuzz.trimf(
            rescue_risk.universe,
            [30, 50, 70]
        )

        rescue_risk["high"] = fuzz.trimf(
            rescue_risk.universe,
            [60, 100, 100]
        )

        return (
            severity,
            hazard,
            distance,
            rescue_risk
        )