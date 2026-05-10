# ============================================
# File: csp/backtracking_solver.py
# Description:
# CSP backtracking solver for constrained
# disaster-response resource allocation.
# ============================================

from csp.forward_checking import (
    ForwardChecking
)

from csp.constraints import (
    ConstraintValidator
)

from csp.mrv_heuristic import (
    MinimumRemainingValues
)


class BacktrackingSolver:
    """
    CSP solver using:
    - Backtracking Search
    - MRV heuristic
    - Degree heuristic tie-breaker
    - Forward checking
    """

    def __init__(
        self,
        ambulances,
        rescue_team,
        total_medical_kits=10
    ):

        self.ambulances = ambulances

        self.rescue_team = rescue_team

        self.total_medical_kits = total_medical_kits

        self.constraint_validator = (
            ConstraintValidator()
        )

        self.solution = None

        self.backtrack_count = 0

    def get_required_kits(
        self,
        victim
    ):
        """
        Kit demand is severity-aware.
        """

        kit_requirements = {

            "critical": 3,
            "moderate": 2,
            "minor": 1
        }

        return kit_requirements.get(
            victim.severity,
            1
        )

    def build_csp(
        self,
        victims
    ):
        """
        Formulate CSP variables and domains.
        """

        variables = [

            victim.victim_id

            for victim
            in victims
        ]

        ambulance_ids = [

            ambulance.ambulance_id

            for ambulance
            in self.ambulances
        ]

        domains = {

            victim.victim_id:
            ambulance_ids + ["WAITLIST"]

            for victim
            in victims
        }

        victim_lookup = {

            victim.victim_id: victim

            for victim
            in victims
        }

        kit_requirements = {

            victim.victim_id:
            self.get_required_kits(
                victim
            )

            for victim
            in victims
        }

        degree_map = {

            victim.victim_id:
            len(victims) - 1

            for victim
            in victims
        }

        ambulance_capacities = {

            ambulance.ambulance_id:
            ambulance.capacity

            for ambulance
            in self.ambulances
        }

        return (
            variables,
            domains,
            victim_lookup,
            kit_requirements,
            degree_map,
            ambulance_capacities
        )

    def allocate_resources(
        self,
        victims
    ):
        """
        Allocate ambulance slots, one rescue team
        location, and medical kits.
        """

        for ambulance in self.ambulances:

            ambulance.assigned_victims = []

        self.rescue_team.current_location = None
        self.rescue_team.is_busy = False

        (
            variables,
            domains,
            victim_lookup,
            kit_requirements,
            degree_map,
            ambulance_capacities
        ) = self.build_csp(victims)

        ambulance_loads = {

            ambulance_id: 0

            for ambulance_id
            in ambulance_capacities
        }

        success = self.backtrack(
            variables=variables,
            domains=domains,
            victim_lookup=victim_lookup,
            kit_requirements=kit_requirements,
            degree_map=degree_map,
            ambulance_capacities=ambulance_capacities,
            assignment={},
            kit_distribution={},
            ambulance_loads=ambulance_loads,
            used_kits=0
        )

        if success:

            self.apply_solution(
                victim_lookup
            )

        return success

    def backtrack(
        self,
        variables,
        domains,
        victim_lookup,
        kit_requirements,
        degree_map,
        ambulance_capacities,
        assignment,
        kit_distribution,
        ambulance_loads,
        used_kits
    ):
        """
        Recursive CSP backtracking.
        """

        self.backtrack_count += 1

        if len(assignment) == len(variables):

            rescue_team_location = (
                self.select_rescue_team_location(
                    assignment,
                    victim_lookup
                )
            )

            if not (
                self.constraint_validator
                .validate_no_duplicate_assignment(
                    assignment
                )
            ):

                return False

            if not (
                self.constraint_validator
                .validate_medical_kit_limit(
                    kit_distribution,
                    self.total_medical_kits
                )
            ):

                return False

            if not (
                self.constraint_validator
                .validate_rescue_team_location(
                    rescue_team_location
                )
            ):

                return False

            self.solution = {

                "assignment": assignment.copy(),
                "kit_distribution": kit_distribution.copy(),
                "rescue_team_location": rescue_team_location,
                "used_kits": used_kits,
                "backtracks": self.backtrack_count,
                "variables": {
                    "Ambulance1_Assignment": [],
                    "Ambulance2_Assignment": [],
                    "RescueTeam_Location": rescue_team_location,
                    "MedicalKit_Distribution": kit_distribution.copy()
                }
            }

            for victim_id, ambulance_id in assignment.items():

                if ambulance_id == 1:

                    self.solution["variables"][
                        "Ambulance1_Assignment"
                    ].append(victim_id)

                elif ambulance_id == 2:

                    self.solution["variables"][
                        "Ambulance2_Assignment"
                    ].append(victim_id)

            return True

        variable = (
            MinimumRemainingValues
            .select_unassigned_variable(
                variables,
                domains,
                assignment,
                degree_map
            )
        )

        ordered_values = self.order_domain_values(
            domains[variable],
            ambulance_loads
        )

        for value in ordered_values:

            required_kits = kit_requirements[
                variable
            ]

            next_used_kits = used_kits

            if value != "WAITLIST":

                if (
                    ambulance_loads[value]
                    >=
                    ambulance_capacities[value]
                ):

                    continue

                next_used_kits += required_kits

                if next_used_kits > self.total_medical_kits:

                    continue

            next_assignment = assignment.copy()
            next_assignment[variable] = value

            next_kit_distribution = (
                kit_distribution.copy()
            )

            next_kit_distribution[variable] = (
                0
                if value == "WAITLIST"
                else required_kits
            )

            next_loads = ambulance_loads.copy()

            if value != "WAITLIST":

                next_loads[value] += 1

            remaining_domains = {

                victim_id: domain

                for victim_id, domain
                in domains.items()

                if victim_id not in next_assignment
            }

            pruned_domains = (
                ForwardChecking.prune_domains(
                    domains=remaining_domains,
                    ambulance_loads=next_loads,
                    ambulance_capacities=ambulance_capacities,
                    remaining_kits=(
                        self.total_medical_kits
                        -
                        next_used_kits
                    ),
                    kit_requirements=kit_requirements
                )
            )

            if pruned_domains is None:

                continue

            next_domains = domains.copy()
            next_domains.update(pruned_domains)

            if self.backtrack(
                variables=variables,
                domains=next_domains,
                victim_lookup=victim_lookup,
                kit_requirements=kit_requirements,
                degree_map=degree_map,
                ambulance_capacities=ambulance_capacities,
                assignment=next_assignment,
                kit_distribution=next_kit_distribution,
                ambulance_loads=next_loads,
                used_kits=next_used_kits
            ):

                return True

        return False

    def order_domain_values(
        self,
        domain,
        ambulance_loads
    ):
        """
        Prefer least loaded ambulance before waitlist.
        """

        return sorted(
            domain,
            key=lambda value: (
                value == "WAITLIST",
                ambulance_loads.get(value, 99)
            )
        )

    def select_rescue_team_location(
        self,
        assignment,
        victim_lookup
    ):
        """
        Only one rescue team can occupy one
        active rescue location.
        """

        assigned_victim_ids = [

            victim_id

            for victim_id, ambulance_id
            in assignment.items()

            if ambulance_id != "WAITLIST"
        ]

        if len(assigned_victim_ids) == 0:

            return None

        highest_priority_victim = max(

            assigned_victim_ids,

            key=lambda victim_id:
            victim_lookup[victim_id]
            .get_priority_score()
        )

        return victim_lookup[
            highest_priority_victim
        ].location

    def apply_solution(
        self,
        victim_lookup
    ):
        """
        Apply final CSP assignment to resources.
        """

        assignment = self.solution[
            "assignment"
        ]

        for victim_id, ambulance_id in assignment.items():

            if ambulance_id == "WAITLIST":

                continue

            ambulance = next(

                item

                for item
                in self.ambulances

                if item.ambulance_id == ambulance_id
            )

            ambulance.assign_victim(
                victim_lookup[victim_id]
            )

        rescue_team_location = self.solution[
            "rescue_team_location"
        ]

        if rescue_team_location is not None:

            self.rescue_team.assign_location(
                rescue_team_location
            )
