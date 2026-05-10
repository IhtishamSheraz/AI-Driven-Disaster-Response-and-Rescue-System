# ============================================
# File: csp/resource_allocator.py
# Description:
# High-level CSP resource allocation
# manager for the rescue system.
# ============================================

from resources.ambulance import Ambulance
from resources.rescue_team import RescueTeam

from csp.backtracking_solver import (
    BacktrackingSolver
)

from csp.mrv_heuristic import (
    MinimumRemainingValues
)


class ResourceAllocator:
    """
    Main CSP allocation manager.
    """

    def __init__(self):

        self.ambulances = [

            Ambulance(
                ambulance_id=1
            ),

            Ambulance(
                ambulance_id=2
            )
        ]

        self.rescue_team = (
            RescueTeam(team_id=1)
        )

        self.total_medical_kits = 10

        self.last_solution = None

    def allocate(
        self,
        victims
    ):
        """
        Allocate victims using CSP.
        """

        prioritized_victims = (
            MinimumRemainingValues
            .sort_victims_by_priority(
                victims
            )
        )

        solver = BacktrackingSolver(
            ambulances=self.ambulances,
            rescue_team=self.rescue_team,
            total_medical_kits=(
                self.total_medical_kits
            )
        )

        allocation_successful = (
            solver.allocate_resources(
                prioritized_victims
            )
        )

        self.last_solution = solver.solution

        return (
            allocation_successful,
            self.ambulances
        )
