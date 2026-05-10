# ============================================
# File: environment/victim.py
# Description:
# Victim model.
# ============================================


class Victim:
    """
    Represents disaster victim.
    """

    def __init__(
        self,
        victim_id,
        location,
        severity
    ):

        self.victim_id = victim_id

        self.location = location

        self.severity = severity

        self.is_rescued = False

        self.is_picked = False

        self.is_delivered = False
                # =====================================
        # MEDICAL KIT REQUIREMENT
        # =====================================

        self.medical_kits_required = 1

        if self.severity == "critical":

            self.medical_kits_required = 1

        elif self.severity == "moderate":

            self.medical_kits_required = 1

        else:

            self.medical_kits_required = 0

    def get_priority_score(self):
        """
        Calculate victim priority.
        """

        severity_scores = {

            "critical": 100,

            "moderate": 60,

            "minor": 30
        }

        return severity_scores.get(
            self.severity,
            0
        )