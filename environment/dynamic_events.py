# ============================================
# File: environment/dynamic_events.py
# Description:
# Handles dynamic disaster events.
# ============================================

import random


class DynamicEnvironmentEvents:
    """
    Generates dynamic environment changes.
    """

    def __init__(
        self,
        environment
    ):
        """
        Initialize dynamic events.
        """

        self.environment = environment

        self.last_events = []

    def trigger_dynamic_cycle(
        self
    ):
        """
        Apply several disaster changes in one
        simulation tick so replanning is tested
        against a changing map.
        """

        events = []

        restored_ambulances = (
            self.environment
            .update_ambulance_availability()
        )

        for ambulance_id in restored_ambulances:

            events.append(
                f"Ambulance A{ambulance_id} restored"
            )

        new_victim = (
            self.environment
            .generate_aftershock_event()
        )

        events.append(
            f"Aftershock: V{new_victim.victim_id} at {new_victim.location}"
        )

        blocked_road = (
            self.environment
            .generate_blocked_road_event()
        )

        if blocked_road is not None:

            events.append(
                f"Road blocked at {blocked_road}"
            )

        fire_position = (
            self.environment
            .spread_fire_event()
        )

        if fire_position is not None:

            events.append(
                f"Fire spread to {fire_position}"
            )

        collapse_position = (
            self.environment
            .increase_collapse_risk_event()
        )

        if collapse_position is not None:

            events.append(
                f"Collapse risk at {collapse_position}"
            )

        if random.random() < 0.45:

            ambulance_id = (
                self.environment
                .generate_ambulance_unavailable_event()
            )

            if ambulance_id is not None:

                events.append(
                    f"Ambulance A{ambulance_id} unavailable"
                )

        self.last_events = events

        return events

    def trigger_random_road_blockage(
        self
    ):
        """
        Create random blocked road.
        """

        maximum_attempts = 50

        for _ in range(
            maximum_attempts
        ):

            random_position = (

                random.randint(
                    0,
                    self.environment.rows - 1
                ),

                random.randint(
                    0,
                    self.environment.columns - 1
                )
            )

            # =====================================
            # SAFETY CHECKS
            # =====================================

            if (
                random_position
                ==
                self.environment.rescue_base
            ):

                continue

            if (
                random_position
                in
                self.environment.medical_centers
            ):

                continue

            victim_positions = [

                victim.location

                for victim
                in
                self.environment.victims
            ]

            if (
                random_position
                in
                victim_positions
            ):

                continue

            if (
                random_position
                in
                self.environment.blocked_roads
            ):

                continue

            # =====================================
            # ADD BLOCKED ROAD
            # =====================================

            self.environment.blocked_roads.add(
                random_position
            )

            return random_position

        return None

    def spread_fire_hazard(
        self
    ):
        """
        Spread random fire hazard.
        """

        return (
            self.environment
            .spread_fire_event()
        )
