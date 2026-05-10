from skfuzzy import control as ctrl


class FuzzyRules:

    def create_rules(
        self,
        severity,
        hazard,
        distance,
        rescue_risk
    ):

        rules = [

            ctrl.Rule(
                severity["high"]
                &
                hazard["high"],
                rescue_risk["high"]
            ),

            ctrl.Rule(
                severity["medium"]
                &
                hazard["medium"],
                rescue_risk["medium"]
            ),

            ctrl.Rule(
                severity["low"]
                &
                hazard["low"],
                rescue_risk["low"]
            ),

            ctrl.Rule(
                distance["far"]
                &
                hazard["high"],
                rescue_risk["high"]
            ),

            ctrl.Rule(
                distance["near"]
                &
                hazard["low"],
                rescue_risk["low"]
            )
        ]

        return rules