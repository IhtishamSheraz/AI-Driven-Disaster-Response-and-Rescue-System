# ============================================
# File: csp/constraints.py
# Description:
# Contains CSP constraint validation
# functions for resource allocation.
# ============================================


class ConstraintValidator:
    """
    Validates CSP constraints.
    """

    @staticmethod
    def validate_ambulance_capacity(
        ambulance
    ):
        """
        Ensure ambulance capacity
        is not exceeded.
        """

        return (
            len(ambulance.assigned_victims)
            <=
            ambulance.capacity
        )

    @staticmethod
    def validate_rescue_team_usage(
        rescue_team
    ):
        """
        Ensure rescue team handles
        only one location at a time.
        """

        return (
            rescue_team.current_location
            is not None
        )

    @staticmethod
    def validate_no_duplicate_assignment(
        assignment
    ):
        """
        Each victim variable can appear only once
        in ambulance assignments.
        """

        assigned_victims = [

            victim_id

            for victim_id, ambulance_id
            in assignment.items()

            if ambulance_id != "WAITLIST"
        ]

        return len(assigned_victims) == len(
            set(assigned_victims)
        )

    @staticmethod
    def validate_medical_kit_limit(
        kit_distribution,
        total_kits
    ):
        """
        Ensure medical kits do not exceed
        available stock.
        """

        used_kits = sum(
            kit_distribution.values()
        )

        return used_kits <= total_kits

    @staticmethod
    def validate_rescue_team_location(
        rescue_team_location
    ):
        """
        One rescue team means one active rescue
        location at a time.
        """

        return (
            rescue_team_location is None
            or
            isinstance(
                rescue_team_location,
                tuple
            )
        )
