# ============================================
# File: fuzzy_logic/fuzzy_inference_engine.py
# Description:
# Main fuzzy inference engine.
# ============================================

from skfuzzy import control as ctrl

from fuzzy_logic.fuzzy_variables import (
    FuzzyVariables
)

from fuzzy_logic.fuzzy_rules import (
    FuzzyRules
)


class FuzzyInferenceEngine:
    """
    Main fuzzy reasoning engine.
    """

    def __init__(self):

        self.variables = (
            FuzzyVariables()
        )

        (
            self.severity,
            self.hazard,
            self.distance,
            self.rescue_risk

        ) = (
            self.variables
            .create_fuzzy_variables()
        )

        self.rules = (
            FuzzyRules()
            .create_rules(

                self.severity,

                self.hazard,

                self.distance,

                self.rescue_risk
            )
        )

        self.control_system = (
            ctrl.ControlSystem(
                self.rules
            )
        )

    def calculate_rescue_risk(
        self,
        severity,
        hazard,
        distance
    ):
        """
        Calculate uncertain rescue risk.
        """

        simulation = (
            ctrl.ControlSystemSimulation(
                self.control_system
            )
        )

        simulation.input[
            "severity"
        ] = severity

        simulation.input[
            "hazard"
        ] = hazard

        simulation.input[
            "distance"
        ] = distance

        simulation.compute()

        if (
            "rescue_risk"
            not in simulation.output
        ):

            return 50.0

        return float(

            simulation.output[
                "rescue_risk"
            ]
        )