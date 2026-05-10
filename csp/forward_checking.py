# ============================================
# File: csp/forward_checking.py
# Description:
# Implements forward checking for CSP.
# ============================================


class ForwardChecking:
    """
    Forward checking constraint pruning.
    """

    @staticmethod
    def check_ambulance_availability(
        ambulances
    ):
        """
        Ensure at least one ambulance
        can still accept victims.
        """

        for ambulance in ambulances:

            if ambulance.can_accept_more_victims():

                return True

        return False

    @staticmethod
    def prune_domains(
        domains,
        ambulance_loads,
        ambulance_capacities,
        remaining_kits,
        kit_requirements
    ):
        """
        Remove values that can no longer be valid
        for future variables.
        """

        pruned_domains = {}

        for victim_id, domain in domains.items():

            valid_values = []

            required_kits = kit_requirements[
                victim_id
            ]

            for value in domain:

                if value == "WAITLIST":

                    valid_values.append(value)

                    continue

                if (
                    ambulance_loads[value]
                    >=
                    ambulance_capacities[value]
                ):

                    continue

                if required_kits > remaining_kits:

                    continue

                valid_values.append(value)

            if len(valid_values) == 0:

                return None

            pruned_domains[victim_id] = valid_values

        return pruned_domains
