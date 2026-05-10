# ============================================
# File: environment/hazard_zone.py
# Description:
# Represents hazardous zones such as fire
# or structural collapse.
# ============================================


class HazardZone:
    """
    Represents a dangerous area in the map.
    """

    def __init__(self, location, risk_level):

        self.location = location
        self.risk_level = risk_level