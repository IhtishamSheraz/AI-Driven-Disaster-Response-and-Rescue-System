# ============================================
# File: resources/rescue_team.py
# Description:
# Rescue team model responsible for
# handling rescue operations.
# ============================================


class RescueTeam:
    """
    Represents rescue team resource.
    """

    def __init__(self, team_id):

        self.team_id = team_id

        self.current_location = None

        self.is_busy = False

    def assign_location(self, location):
        """
        Assign rescue team to location.
        """

        self.current_location = location

        self.is_busy = True