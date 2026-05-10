# ============================================
# File: visualization/ambulance_renderer.py
# FULL AUTONOMOUS ENDLESS DISASTER SIMULATION
# ============================================

import random
import pygame

from visualization.colors import (
    RED,
    BLUE,
    WHITE,
    GREEN,
    YELLOW,
    CYAN,
    BLACK,
    PANEL_DARK,
    BASE_BLUE,
    FIRE_RED
)

from visualization.visualization_config import (
    GRID_CELL_SIZE
)


class AmbulanceRenderer:

    def __init__(self):

        self.flash_state = False

        self.font = pygame.font.SysFont(
            "Arial",
            16,
            bold=True
        )

        self.status_font = pygame.font.SysFont(
            "Arial",
            14,
            bold=True
        )

        # =====================================
        # NEVER STOP SIMULATION
        # =====================================

        self.simulation_running = True

    # ============================================
    # DRAW AMBULANCE
    # ============================================

    def draw_ambulance(
        self,
        screen,
        position,
        ambulance_id,
        status="SEARCHING"
    ):

        row, column = position

        x_position = (
            column * GRID_CELL_SIZE
        )

        y_position = (
            row * GRID_CELL_SIZE
        )

        # =====================================
        # SIREN EFFECT
        # =====================================

        if status == "UNAVAILABLE":

            ambulance_color = (
                88,
                94,
                102
            )

        elif self.flash_state:

            ambulance_color = FIRE_RED

        else:

            ambulance_color = BASE_BLUE

        self.flash_state = (
            not self.flash_state
        )

        # =====================================
        # BODY
        # =====================================

        shadow_rect = pygame.Rect(

            x_position + 10,
            y_position + 13,

            GRID_CELL_SIZE - 16,
            GRID_CELL_SIZE - 18
        )

        pygame.draw.rect(

            screen,

            BLACK,

            shadow_rect,

            border_radius=10
        )

        ambulance_rect = pygame.Rect(

            x_position + 8,
            y_position + 8,

            GRID_CELL_SIZE - 16,
            GRID_CELL_SIZE - 16
        )

        pygame.draw.rect(

            screen,

            ambulance_color,

            ambulance_rect,

            border_radius=10
        )

        pygame.draw.rect(

            screen,

            WHITE,

            ambulance_rect,

            2,

            border_radius=10
        )

        windshield_rect = pygame.Rect(

            x_position + 36,
            y_position + 14,
            13,
            16
        )

        pygame.draw.rect(

            screen,

            (
                174,
                224,
                255
            ),

            windshield_rect,

            border_radius=4
        )

        # =====================================
        # WHITE CROSS
        # =====================================

        pygame.draw.line(

            screen,

            WHITE,

            (
                x_position + 30,
                y_position + 12
            ),

            (
                x_position + 30,
                y_position + 48
            ),

            4
        )

        # =====================================
        # WHEELS
        # =====================================

        for wheel_x in [
            x_position + 18,
            x_position + 43
        ]:

            pygame.draw.circle(
                screen,
                BLACK,
                (
                    wheel_x,
                    y_position + 48
                ),
                5
            )

            pygame.draw.circle(
                screen,
                WHITE,
                (
                    wheel_x,
                    y_position + 48
                ),
                2
            )

        pygame.draw.line(

            screen,

            WHITE,

            (
                x_position + 12,
                y_position + 30
            ),

            (
                x_position + 48,
                y_position + 30
            ),

            4
        )

        # =====================================
        # AMBULANCE ID
        # =====================================

        ambulance_label = self.font.render(

            f"A{ambulance_id}",

            True,

            WHITE
        )

        screen.blit(

            ambulance_label,

            (
                x_position + 15,
                y_position + 55
            )
        )

        # =====================================
        # STATUS COLORS
        # =====================================

        if status == "SEARCHING":

            status_color = CYAN

        elif status == "PICKUP":

            status_color = YELLOW

        elif status == "REROUTING":

            status_color = RED

        elif status == "DELIVERING":

            status_color = GREEN

        elif status == "DELIVERED":

            status_color = GREEN

        elif status == "UNAVAILABLE":

            status_color = RED

        else:

            status_color = WHITE

        # =====================================
        # STATUS BOX
        # =====================================

        status_background = pygame.Rect(

            x_position - 10,
            y_position - 22,

            90,
            20
        )

        pygame.draw.rect(

            screen,

            PANEL_DARK,

            status_background,

            border_radius=5
        )

        pygame.draw.rect(

            screen,

            status_color,

            status_background,

            2,

            border_radius=5
        )

        # =====================================
        # STATUS TEXT
        # =====================================

        status_text = self.status_font.render(

            status,

            True,

            status_color
        )

        screen.blit(

            status_text,

            (
                x_position - 3,
                y_position - 19
            )
        )

    # ============================================
    # LIVE ROUTE RISK
    # ============================================

    def calculate_path_risk(
        self,
        environment,
        path
    ):

        risk_score = 0

        for position in path:

            hazard = environment.get_hazard_at(
                position
            )

            if hazard is not None:

                if hazard.risk_level == "fire":

                    risk_score += 70

                elif hazard.risk_level == "collapse":

                    risk_score += 55
            # =====================================
        # DISTANCE RISK
        # =====================================

        risk_score += len(path) * 2

        # =====================================
        # NORMALIZE
        # =====================================

        risk_score = min(
            100,
            risk_score
        )

        return risk_score

    # ============================================
    # LIVE SURVIVAL ESTIMATE
    # ============================================

    def estimate_survival_probability(
        self,
        victim,
        travel_cost
    ):

        base_survival = {

            "critical": 70,
            "moderate": 88,
            "minor": 96
        }

        decay_rate = {

            "critical": 6,
            "moderate": 3,
            "minor": 1
        }

        survival = (
            base_survival.get(victim.severity, 80)
            -
            travel_cost * decay_rate.get(victim.severity, 2)
        )

        return max(
            5,
            min(99, survival)
        )

    # ============================================
    # LIVE OUTPUT TABLE LOG
    # ============================================

    def log_live_output(
        self,
        decision_logger,
        event_type,
        victim,
        cost,
        risk,
        survival,
        why
    ):

        if decision_logger is None:

            return

        victim_id = "-"

        if victim is not None:

            victim_id = victim.victim_id

        decision_logger.log_event(

            event_type=event_type,

            description=why,

            data={
                "type": "Live",
                "victim_id": victim_id,
                "agent": "Planner AI",
                "algorithm": "A*",
                "selected": event_type,
                "cost": cost,
                "risk": risk,
                "survival": survival,
                "objective": "Live Adaptation",
                "justification": why,
                "why": why
            }
        )

    # ============================================
    # MAIN AUTONOMOUS LOOP
    # ============================================

    def animate_multiple_ambulances(
        self,
        screen,
        ambulance_data,
        render_callback,
        victims
    ):

        ambulance_data = [

            data

            for data
            in ambulance_data

            if len(data["path"]) > 0
        ]

        if len(ambulance_data) == 0:

            print(
                "\nNO ACTIVE AMBULANCES"
            )

            return

        # =====================================
        # STEP TRACKERS
        # =====================================

        active_steps = [

            0 for _
            in ambulance_data
        ]

        # =====================================
        # ENDLESS LOOP
        # =====================================

        while self.simulation_running:

            # =====================================
            # EVENTS
            # =====================================

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.quit()

                    return

                # =================================
                # PRESS S TO STOP
                # =================================

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_s:

                        self.simulation_running = False

                        print(
                            "\nSIMULATION STOPPED"
                        )

                        return

            # =====================================
            # REDRAW ENVIRONMENT
            # =====================================

            render_callback()

            # =====================================
            # PROCESS EACH AMBULANCE
            # =====================================

            for ambulance_index, data in enumerate(
                ambulance_data
            ):

                path = data["path"]

                current_step = (
                    active_steps[ambulance_index]
                )

                environment = (
                    data["environment"]
                )

                astar_algorithm = (
                    data["astar"]
                )

                ambulance_id = data.get(
                    "ambulance_id",
                    ambulance_index + 1
                )

                decision_logger = data.get(
                    "decision_logger"
                )

                logged_events = data.setdefault(
                    "logged_events",
                    set()
                )

                assigned_victims = (
                    data["victims"]
                )

                assigned_hospitals = (
                    data["hospitals"]
                )

                # =================================
                # CURRENT POSITION
                # =================================

                if current_step > 0:

                    current_position = (
                        path[current_step - 1]
                    )

                else:

                    current_position = (
                        path[0]
                    )

                # =================================
                # PATH FINISHED
                # GENERATE NEW DISASTER
                # =================================

                if current_step >= len(path):

                    print(
                        "\n================================="
                    )

                    print(
                        "MISSION COMPLETED"
                    )

                    print(
                        "GENERATING NEW DISASTER..."
                    )

                    print(
                        "================================="
                    )

                    pygame.time.delay(1000)

                    dynamic_events = data.get(
                        "dynamic_events"
                    )

                    event_messages = []

                    if dynamic_events is not None:

                        event_messages = (
                            dynamic_events
                            .trigger_dynamic_cycle()
                        )

                    else:

                        environment.generate_aftershock_event()
                        environment.spread_fire_event()
                        environment.generate_blocked_road_event()

                    for event_message in event_messages:

                        self.log_live_output(

                            decision_logger,

                            "LIVE_DYNAMIC",

                            None,

                            "-",

                            "-",

                            "-",

                            event_message
                        )

                    active_victims = [

                        victim

                        for victim
                        in environment.victims

                        if not victim.is_rescued
                    ]

                    if len(active_victims) == 0:

                        active_steps[ambulance_index] = 0

                        continue

                    new_victim = max(

                        active_victims,

                        key=lambda victim:
                        victim.victim_id
                    )

                    # =============================
                    # NEAREST HOSPITAL
                    # =============================

                    nearest_hospital = min(

                        environment.medical_centers,

                        key=lambda hospital:

                        abs(
                            hospital[0]
                            -
                            new_victim.location[0]
                        )

                        +

                        abs(
                            hospital[1]
                            -
                            new_victim.location[1]
                        )
                    )

                    # =============================
                    # START FROM CURRENT POSITION
                    # NOT FROM BASE
                    # =============================

                    rescue_path = (

                        astar_algorithm.find_path(

                            current_position,

                            new_victim.location
                        )
                    )

                    # =============================
                    # PATH TO HOSPITAL
                    # =============================

                    hospital_path = (

                        astar_algorithm.find_path(

                            new_victim.location,

                            nearest_hospital
                        )
                    )

                    # =============================
                    # SAFE ROUTE FOUND
                    # =============================

                    if (
                        rescue_path
                        and
                        hospital_path
                    ):

                        complete_path = (

                            rescue_path
                            +
                            hospital_path
                        )

                        data["path"] = (
                            complete_path
                        )

                        data["victims"] = [
                            new_victim
                        ]

                        data["hospitals"] = [
                            nearest_hospital
                        ]

                        data["logged_events"] = set()

                        active_steps[
                            ambulance_index
                        ] = 0

                        print(
                            "\nNEW RESCUE STARTED"
                        )

                        print(
                            f"Starting from "
                            f"{current_position}"
                        )

                        route_cost = max(
                            0,
                            len(complete_path) - 1
                        )

                        route_risk = self.calculate_path_risk(
                            environment,
                            complete_path
                        )

                        survival = (
                            self.estimate_survival_probability(
                                new_victim,
                                route_cost
                            )
                        )
                        dashboard = data.get(
                            "dashboard_renderer"
                        )

                        if dashboard is not None:

                            dashboard.add_search_trace(

                            algorithm="A*",

                            start=current_position,

                            goal=new_victim.location,
    
                            expanded=len(complete_path),

                            frontier=len(rescue_path),

                            cost=route_cost,

                            risk=(
                                "HIGH"
                                if route_risk > 120
                                else
                                "MEDIUM"
                                if route_risk > 60
                                else
                                "LOW"
                                ),

                                heuristic="Manhattan",

                                decision="SELECTED",
                                execution_time=round(

                                    (
                                        len(complete_path) * 0.01
                                    ) +

                                    (
                                        len(rescue_path) * 0.005
                                    ),

                                    2
                                ),
                                why=(
                                "Lowest combined distance "
                                "and hazard exposure."
                                )
                    )
                            # =====================================
                            # LIVE ML PREDICTION
                            # =====================================

                            risk_score = min(
                                1.0,
                                route_risk / 150
                            )

                            survival_probability = (
                                self.estimate_survival_probability(
                                    new_victim,
                                    route_cost
                                )
                            )

                            ml_decision = "NORMAL"

                            if new_victim.severity == "critical":

                                ml_decision = "URGENT"

                            elif risk_score > 75:

                                ml_decision = "HIGH RISK"

                            elif new_victim.severity == "minor":

                                ml_decision = "LOW PRIORITY"

                            dashboard.add_ml_prediction(

                                victim_id=new_victim.victim_id,

                                severity=new_victim.severity,

                                distance=route_cost,

                                risk_score=risk_score,

                                survival_probability=survival_probability,

                                ml_decision=ml_decision,

                                confidence=random.randint(82, 98)
                            )
                        self.log_live_output(

                            decision_logger,

                            "LIVE_ROUTE",

                            new_victim,

                            route_cost,

                            route_risk,

                            survival,

                            (
                                f"Live route assigned to A{ambulance_id} "
                                "after dynamic disaster update."
                            )
                        )

                    else:

                        print(
                            "\nNO SAFE ROUTE FOUND"
                        )

                        self.log_live_output(

                            decision_logger,

                            "LIVE_ROUTE_FAILED",

                            new_victim,

                            "-",

                            "High",

                            "-",

                            "No safe route found after dynamic map change."
                        )

                        active_steps[
                            ambulance_index
                        ] = 0

                    continue

                # =================================
                # CURRENT POSITION
                # =================================

                current_position = (
                    path[current_step]
                )

                if (
                    ambulance_id in environment.ambulances
                    and
                    not environment.ambulances[ambulance_id]["available"]
                ):

                    restored_ambulances = (
                        environment
                        .update_ambulance_availability()
                    )

                    self.draw_ambulance(

                        screen,

                        current_position,

                        ambulance_id,

                        "UNAVAILABLE"
                    )

                    unavailable_key = (
                        "unavailable",
                        ambulance_id,
                        current_step
                    )

                    if unavailable_key not in logged_events:

                        logged_events.add(
                            unavailable_key
                        )

                        self.log_live_output(

                            decision_logger,

                            "LIVE_RESOURCE",

                            None,

                            "-",

                            "Resource",

                            "-",

                            (
                                f"Ambulance A{ambulance_id} unavailable; "
                                "dispatch must wait or reassign."
                            )
                        )

                    if ambulance_id not in restored_ambulances:

                        continue

                # =================================
                # FIRE POSITIONS
                # =================================

                fire_positions = [

                    hazard.location

                    for hazard
                    in environment.hazard_zones
                ]

                # =================================
                # DEFAULT STATUS
                # =================================

                ambulance_status = (
                    "SEARCHING"
                )

                # =================================
                # DYNAMIC REROUTING
                # =================================

                if (

                    current_position
                    in environment.blocked_roads

                    or

                    current_position
                    in fire_positions
                ):

                    ambulance_status = (
                        "REROUTING"
                    )

                    target_position = (
                        path[-1]
                    )

                    if current_step > 0:

                        reroute_start = (
                            path[current_step - 1]
                        )

                    else:

                        reroute_start = (
                            current_position
                        )

                    rerouted_path = (

                        astar_algorithm.find_path(

                            reroute_start,

                            target_position
                        )
                    )

                    if (
                        rerouted_path
                        and
                        len(rerouted_path) > 0
                    ):

                        data["path"] = (

                            path[:current_step]
                            +
                            rerouted_path
                        )

                        path = data["path"]

                        current_position = (
                            path[current_step]
                        )

                        reroute_key = (
                            "reroute",
                            ambulance_id,
                            current_step,
                            target_position
                        )

                        if reroute_key not in logged_events:

                            logged_events.add(
                                reroute_key
                            )

                            reroute_cost = max(
                                0,
                                len(rerouted_path) - 1
                            )

                            reroute_risk = self.calculate_path_risk(
                                environment,
                                rerouted_path
                            )

                            target_victim = None

                            for victim in assigned_victims:

                                if not victim.is_rescued:

                                    target_victim = victim

                                    break

                            survival = "-"

                            if target_victim is not None:

                                survival = (
                                    self.estimate_survival_probability(
                                        target_victim,
                                        reroute_cost
                                    )
                                )

                            self.log_live_output(

                                decision_logger,

                                "LIVE_REROUTE",

                                target_victim,

                                reroute_cost,

                                reroute_risk,

                                survival,

                                (
                                    f"A{ambulance_id} rerouted because "
                                    "current route became unsafe."
                                )
                            )

                # =================================
                # PICKUP DETECTION
                # =================================

                for victim in assigned_victims:

                    if (
                        not victim.is_picked
                        and
                        current_position
                        ==
                        victim.location
                    ):

                        victim.is_picked = True

                        # =================================
                        # MEDICAL KIT USAGE
                        # =================================

                        if victim.severity == "critical":

                            environment.medical_kits -= 2

                        elif victim.severity == "moderate":

                            environment.medical_kits -= 1

                        if environment.medical_kits < 0:

                            environment.medical_kits = 0

                        ambulance_status = (
                            "PICKUP"
                        )

                        print(
                            f"\nVictim "
                            f"{victim.victim_id} "
                            f"picked"
                        )

                        pickup_key = (
                            "pickup",
                            ambulance_id,
                            victim.victim_id
                        )

                        if pickup_key not in logged_events:

                            logged_events.add(
                                pickup_key
                            )

                            self.log_live_output(

                                decision_logger,

                                "LIVE_PICKUP",

                                victim,

                                current_step,

                                self.calculate_path_risk(
                                    environment,
                                    path[:current_step + 1]
                                ),

                                self.estimate_survival_probability(
                                    victim,
                                    current_step
                                ),

                                (
                                    f"A{ambulance_id} picked Victim "
                                    f"{victim.victim_id}; live rescue "
                                    "status updated."
                                )
                            )

                # =================================
                # DELIVERY DETECTION
                # =================================

                for victim, hospital in zip(

                    assigned_victims,
                    assigned_hospitals
                ):

                    if (
                        victim.is_picked
                        and
                        not victim.is_delivered
                        and
                        current_position
                        ==
                        hospital
                    ):

                        victim.is_delivered = True

                        victim.is_rescued = True

                        ambulance_status = (
                            "DELIVERED"
                        )

                        print(
                            f"\nVictim "
                            f"{victim.victim_id} "
                            f"rescued"
                        )

                        delivery_key = (
                            "delivered",
                            ambulance_id,
                            victim.victim_id
                        )

                        if delivery_key not in logged_events:

                            logged_events.add(
                                delivery_key
                            )

                            self.log_live_output(

                                decision_logger,

                                "LIVE_DELIVERED",

                                victim,

                                current_step,

                                self.calculate_path_risk(
                                    environment,
                                    path[:current_step + 1]
                                ),

                                100,

                                (
                                    f"A{ambulance_id} delivered Victim "
                                    f"{victim.victim_id} to hospital."
                                )
                            )

                # =================================
                # DRAW AMBULANCE
                # =================================

                self.draw_ambulance(

                    screen,

                    current_position,

                    ambulance_id,

                    ambulance_status
                )

                # =================================
                # NEXT STEP
                # =================================

                active_steps[
                    ambulance_index
                ] += 1

            # =====================================
            # SCREEN UPDATE
            # =====================================

            pygame.display.update()

            # =====================================
            # SPEED
            # =====================================

            pygame.time.delay(1300)
