# ============================================
# File: resources/ambulance.py
# Description:
# Ambulance resource model used for
# victim transportation.
# ============================================


class Ambulance:
    """
    Represents an ambulance resource.
    """

    def __init__(
        self,
        ambulance_id,
        capacity=2
    ):

        self.ambulance_id = ambulance_id

        self.capacity = capacity

        self.assigned_victims = []

    def can_accept_more_victims(self):
        """
        Check whether ambulance has
        remaining capacity.
        """

        return (
            len(self.assigned_victims)
            <
            self.capacity
        )

    def assign_victim(self, victim):
        """
        Assign victim to ambulance.
        """

        self.assigned_victims.append(victim)