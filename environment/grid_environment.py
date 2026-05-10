# ============================================
# File: environment/grid_environment.py
# ============================================

import random

from environment.victim import Victim
from environment.hazard_zone import HazardZone


class GridEnvironment:

    def __init__(
        self,
        rows=10,
        columns=10
    ):

        self.rows = rows
        self.columns = columns
        self.medical_kits = 10

        # =====================================
        # RESCUE BASE
        # =====================================

        self.rescue_base = (0, 0)

        # =====================================
        # HOSPITALS
        # =====================================

        self.medical_centers = [

            (9, 9),
            (0, 9)
        ]

        self.safe_zones = (
            self.medical_centers
        )

        # =====================================
        # AMBULANCES
        # =====================================

        self.ambulances = {

            1: {
                "available": True,
                "unavailable_ticks": 0
            },

            2: {
                "available": True,
                "unavailable_ticks": 0
            }
        }

        # =====================================
        # BLOCKED ROADS
        # =====================================

        self.blocked_roads = {

            (2, 2),
            (2, 3),
            (3, 3),
            (4, 5),
            (5, 5)
        }

        # =====================================
        # HAZARDS
        # =====================================

        self.hazard_zones = [

            HazardZone(
                (4, 4),
                "fire"
            ),

            HazardZone(
                (6, 2),
                "collapse"
            )
        ]

        # =====================================
        # VICTIMS
        # =====================================

        self.victims = [

            Victim(
                1,
                (1, 7),
                "critical"
            ),

            Victim(
                2,
                (5, 8),
                "critical"
            ),

            Victim(
                3,
                (8, 1),
                "moderate"
            ),

            Victim(
                4,
                (7, 5),
                "moderate"
            ),

            Victim(
                5,
                (3, 8),
                "minor"
            )
        ]

    # ============================================
    # CHECK GRID
    # ============================================

    def is_position_inside_grid(
        self,
        position
    ):

        row, column = position

        return (

            0 <= row < self.rows
            and
            0 <= column < self.columns
        )

    # ============================================
    # CHECK BLOCKED ROAD
    # ============================================

    def is_position_blocked(
        self,
        position
    ):

        return (
            position
            in
            self.blocked_roads
        )

    # ============================================
    # CHECK HAZARD
    # ============================================

    def is_hazard_position(
        self,
        position
    ):

        for hazard in self.hazard_zones:

            if (
                hazard.location
                ==
                position
            ):

                return True

        return False

    # ============================================
    # HAZARD TYPE CHECK
    # ============================================

    def get_hazard_at(
        self,
        position
    ):

        for hazard in self.hazard_zones:

            if hazard.location == position:

                return hazard

        return None

    # ============================================
    # VALID POSITION
    # ============================================

    def is_valid_position(
        self,
        position
    ):

        if not self.is_position_inside_grid(
            position
        ):

            return False

        # =====================================
        # BLOCKED ROAD
        # =====================================

        if self.is_position_blocked(
            position
        ):

            return False

        # =====================================
        # FIRE / HAZARD
        # =====================================

        if self.is_hazard_position(
            position
        ):

            return False

        return True

    # ============================================
    # SAFE NEIGHBORS
    # ============================================

    def get_neighbors(
        self,
        current_position
    ):

        row, column = current_position

        possible_moves = [

            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        valid_neighbors = []

        for row_change, column_change in possible_moves:

            new_row = (
                row + row_change
            )

            new_column = (
                column + column_change
            )

            new_position = (

                new_row,
                new_column
            )

            if not self.is_valid_position(
                new_position
            ):

                continue

            valid_neighbors.append(
                new_position
            )

        return valid_neighbors

    # ============================================
    # RANDOM SAFE POSITION
    # ============================================

    def generate_random_position(
        self
    ):

        while True:

            random_position = (

                random.randint(
                    0,
                    self.rows - 1
                ),

                random.randint(
                    0,
                    self.columns - 1
                )
            )

            # =================================
            # VALID POSITION
            # =================================

            if not self.is_valid_position(
                random_position
            ):

                continue

            # =================================
            # AVOID RESCUE BASE
            # =================================

            if (
                random_position
                ==
                self.rescue_base
            ):

                continue

            # =================================
            # AVOID HOSPITALS
            # =================================

            if (
                random_position
                in self.medical_centers
            ):

                continue

            # =================================
            # AVOID VICTIMS
            # =================================

            victim_positions = [

                victim.location

                for victim
                in self.victims

                if not victim.is_rescued
            ]

            if random_position in victim_positions:

                continue

            return random_position

    # ============================================
    # RANDOM ROAD POSITION
    # ============================================

    def generate_random_road_position(
        self
    ):

        maximum_attempts = 100

        for _ in range(maximum_attempts):

            random_position = (

                random.randint(
                    0,
                    self.rows - 1
                ),

                random.randint(
                    0,
                    self.columns - 1
                )
            )

            if random_position == self.rescue_base:

                continue

            if random_position in self.medical_centers:

                continue

            if random_position in self.blocked_roads:

                continue

            if self.is_hazard_position(random_position):

                continue

            return random_position

        return None

    # ============================================
    # FREE NEIGHBORS FOR SPREADING
    # ============================================

    def get_free_adjacent_positions(
        self,
        position
    ):

        row, column = position

        candidates = [

            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1)
        ]

        free_positions = []

        for candidate in candidates:

            if not self.is_position_inside_grid(candidate):

                continue

            if candidate == self.rescue_base:

                continue

            if candidate in self.medical_centers:

                continue

            if candidate in self.blocked_roads:

                continue

            if self.is_hazard_position(candidate):

                continue

            victim_positions = [

                victim.location

                for victim
                in self.victims

                if not victim.is_rescued
            ]

            if candidate in victim_positions:

                continue

            free_positions.append(candidate)

        return free_positions

    # ============================================
    # AVAILABLE AMBULANCES
    # ============================================

    def get_available_ambulance_ids(
        self
    ):

        return [

            ambulance_id

            for ambulance_id, ambulance
            in self.ambulances.items()

            if ambulance["available"]
        ]

    # ============================================
    # RESTORE AMBULANCES
    # ============================================

    def update_ambulance_availability(
        self
    ):

        restored_ambulances = []

        for ambulance_id, ambulance in self.ambulances.items():

            if ambulance["available"]:

                continue

            ambulance["unavailable_ticks"] -= 1

            if ambulance["unavailable_ticks"] <= 0:

                ambulance["available"] = True
                ambulance["unavailable_ticks"] = 0
                restored_ambulances.append(ambulance_id)

        return restored_ambulances

    # ============================================
    # AFTERSHOCK EVENT
    # ============================================

    def generate_aftershock_event(
        self
    ):

        victim_position = (
            self.generate_random_position()
        )

        severity_levels = [

            "critical",
            "moderate",
            "minor"
        ]

        new_victim = Victim(

            victim_id=(
                len(self.victims) + 1
            ),

            location=victim_position,

            severity=random.choice(
                severity_levels
            )
        )

        self.victims.append(
            new_victim
        )

        print(
            "\nAFTERSHOCK OCCURRED"
        )

        print(
            f"New victim at "
            f"{victim_position}"
        )

        return new_victim

    # ============================================
    # FIRE EVENT
    # ============================================

    def generate_fire_event(
        self
    ):

        fire_position = (
            self.generate_random_position()
        )

        new_fire = HazardZone(

            fire_position,

            "fire"
        )

        self.hazard_zones.append(
            new_fire
        )

        print(
            f"\nFIRE EVENT "
            f"AT {fire_position}"
        )

        return fire_position

    # ============================================
    # SPREAD FIRE EVENT
    # ============================================

    def spread_fire_event(
        self
    ):

        fire_zones = [

            hazard

            for hazard
            in self.hazard_zones

            if hazard.risk_level == "fire"
        ]

        random.shuffle(fire_zones)

        for fire_zone in fire_zones:

            free_positions = self.get_free_adjacent_positions(
                fire_zone.location
            )

            if len(free_positions) == 0:

                continue

            new_position = random.choice(
                free_positions
            )

            self.hazard_zones.append(
                HazardZone(
                    new_position,
                    "fire"
                )
            )

            print(
                f"\nFIRE SPREAD TO {new_position}"
            )

            return new_position

        return self.generate_fire_event()

    # ============================================
    # COLLAPSE RISK EVENT
    # ============================================

    def increase_collapse_risk_event(
        self
    ):

        collapse_zones = [

            hazard

            for hazard
            in self.hazard_zones

            if hazard.risk_level == "collapse"
        ]

        random.shuffle(collapse_zones)

        for collapse_zone in collapse_zones:

            free_positions = self.get_free_adjacent_positions(
                collapse_zone.location
            )

            if len(free_positions) == 0:

                continue

            new_position = random.choice(
                free_positions
            )

            self.hazard_zones.append(
                HazardZone(
                    new_position,
                    "collapse"
                )
            )

            print(
                f"\nCOLLAPSE RISK EXPANDED TO {new_position}"
            )

            return new_position

        risk_position = self.generate_random_road_position()

        if risk_position is None:

            return None

        self.hazard_zones.append(
            HazardZone(
                risk_position,
                "collapse"
            )
        )

        print(
            f"\nNEW COLLAPSE ZONE AT {risk_position}"
        )

        return risk_position

    # ============================================
    # BLOCKED ROAD EVENT
    # ============================================

    def generate_blocked_road_event(
        self
    ):

        while True:

            blocked_position = (

                random.randint(
                    0,
                    self.rows - 1
                ),

                random.randint(
                    0,
                    self.columns - 1
                )
            )

            # =================================
            # AVOID BASE
            # =================================

            if (
                blocked_position
                ==
                self.rescue_base
            ):

                continue

            # =================================
            # AVOID HOSPITALS
            # =================================

            if (
                blocked_position
                in self.medical_centers
            ):

                continue

            # =================================
            # AVOID EXISTING BLOCKS
            # =================================

            if (
                blocked_position
                in self.blocked_roads
            ):

                continue

            # =================================
            # AVOID HAZARDS
            # =================================

            hazard_positions = [

                hazard.location

                for hazard
                in self.hazard_zones
            ]

            if (
                blocked_position
                in hazard_positions
            ):

                continue

            # =================================
            # ADD BLOCKED ROAD
            # =================================

            self.blocked_roads.add(
                blocked_position
            )

            print(
                f"\nBLOCKED ROAD "
                f"AT {blocked_position}"
            )

            return blocked_position

    # ============================================
    # AMBULANCE UNAVAILABLE EVENT
    # ============================================

    def generate_ambulance_unavailable_event(
        self
    ):

        available_ambulances = self.get_available_ambulance_ids()

        if len(available_ambulances) == 0:

            return None

        ambulance_id = random.choice(
            available_ambulances
        )

        self.ambulances[ambulance_id]["available"] = False
        self.ambulances[ambulance_id]["unavailable_ticks"] = random.randint(
            1,
            3
        )

        print(
            f"\nAMBULANCE A{ambulance_id} UNAVAILABLE"
        )

        return ambulance_id
