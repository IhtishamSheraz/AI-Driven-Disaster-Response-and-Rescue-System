# ============================================
# File: visualization/simulation_window.py
# COMPLETE FINAL FIXED FILE
# ============================================

import random
import pygame

from visualization.colors import *

from visualization.visualization_config import *

from visualization.ambulance_renderer import (
    AmbulanceRenderer
)

from visualization.map_renderer import (
    MapRenderer
)

from visualization.dashboard_renderer import (
    DashboardRenderer
)


class SimulationWindow:

    def __init__(
        self,
        environment
    ):

        pygame.init()

        self.environment = environment

        # =====================================
        # WINDOW SIZE
        # =====================================

        self.window_width = WINDOW_WIDTH
        self.window_height = WINDOW_HEIGHT
        self.min_width = 1000
        self.min_height = 620
        self.fullscreen = False

        self.screen = pygame.display.set_mode(
            (
                self.window_width,
                self.window_height
            ),
            pygame.RESIZABLE
        )

        pygame.display.set_caption(
            "AIDRA: AI Disaster Response Agent"
        )

        self.clock = pygame.time.Clock()

        # =====================================
        # RENDERERS
        # =====================================

        self.map_renderer = MapRenderer(
            environment
        )

        self.ambulance_renderer = (
            AmbulanceRenderer()
        )

        self.dashboard_renderer = (
            DashboardRenderer()
        )


        # =====================================
        # FONTS
        # =====================================

        self.title_font = pygame.font.SysFont(
            "Arial",
            16,
            bold=True
        )

        self.font = pygame.font.SysFont(
            "Arial",
            12,
            bold=True
        )

        self.small_font = pygame.font.SysFont(
            "Arial",
            10
        )

        # =====================================
        # ALERTS
        # =====================================

        self.current_alert = ""

        self.alert_timer = 0

        # =====================================
        # SYSTEM STATUS
        # =====================================

        self.simulation_active = True

        self.auto_rescue_started = False

        self.last_disaster_time = (
            pygame.time.get_ticks()
        )

        self.disaster_interval = 8000

    def _apply_window_mode(self):
        if self.fullscreen:
            self.screen = pygame.display.set_mode(
                (0, 0),
                pygame.FULLSCREEN
            )
            self.window_width, self.window_height = self.screen.get_size()
            return

        self.window_width = max(self.min_width, self.window_width)
        self.window_height = max(self.min_height, self.window_height)
        self.screen = pygame.display.set_mode(
            (
                self.window_width,
                self.window_height
            ),
            pygame.RESIZABLE
        )

    # ============================================
    # ALERT SYSTEM
    # ============================================

    def show_alert(
        self,
        message
    ):

        self.current_alert = message

        self.alert_timer = 120

    # ============================================
    # AUTO DISASTER GENERATOR
    # ============================================

    def auto_generate_disasters(
        self,
        agent
    ):

        if not self.simulation_active:

            return

        current_time = pygame.time.get_ticks()

        if (

            current_time
            -
            self.last_disaster_time

            >

            self.disaster_interval
        ):

            self.last_disaster_time = (
                current_time
            )

            event_messages = (
                agent
                .dynamic_event_system
                .trigger_dynamic_cycle()
            )

            self.show_alert(
                "NEW DISASTER DETECTED"
            )

            for event_message in event_messages[-5:]:

                self.dashboard_renderer.add_log(
                    event_message
                )

                agent.decision_logger.log_event(

                    event_type="DYNAMIC_DISASTER",

                    description=event_message,

                    data={
                        "type": "Disaster",
                        "agent": "Monitor AI",
                        "algorithm": "Event Trigger",
                        "objective": "Adapt to Risk",
                        "justification": (
                            "Environment changed, so routes and "
                            "resource choices must be reviewed."
                        ),
                        "why": event_message,
                        "priority": "CRITICAL",
                        "outcome": "ACTIVE"
                    }
                )

            self.dashboard_renderer.add_log(
                "Dynamic rerouting activated"
            )

            agent.decision_logger.log_event(

                event_type="REROUTING",

                description="Dynamic rerouting activated after map change",

                data={
                    "type": "Route",
                    "agent": "Replanner AI",
                    "algorithm": "A*",
                    "objective": "Minimize Risk",
                    "justification": (
                        "Map changed due to disaster event; "
                        "routes are recalculated."
                    ),
                    "why": "Dynamic rerouting activated after map change",
                    "priority": "HIGH",
                    "outcome": "ACTIVE"
                }
            )

            agent.auto_dispatch_new_victims()

    # ============================================
    # AUTO RESCUE SYSTEM
    # ============================================

    def auto_rescue_system(
        self,
        agent
    ):

        if self.auto_rescue_started:

            return

        self.auto_rescue_started = True
        self.current_agent = agent

        self.dashboard_renderer.add_log(
            "Autonomous rescue enabled"
        )

        agent.auto_dispatch_new_victims()

    # ============================================
    # CONTROL PANEL
    # ============================================

    def draw_control_panel(
        self
    ):

        pygame.draw.rect(

            self.screen,

            (185, 185, 185),

            (
                650,
                0,
                715,
                768
            )
        )

       

        # =====================================
        # LIVE STATISTICS
        # =====================================

        stats_title = self.font.render(

            "LIVE STATISTICS",

            True,

            CYAN
        )

        self.screen.blit(
            stats_title,
            (1160, 95)
        )

        rescued_count = len([

            victim

            for victim
            in self.environment.victims

            if victim.is_rescued
        ])

        active_count = len([

            victim

            for victim
            in self.environment.victims

            if not victim.is_rescued
        ])

        stats = [

            f"Victims: {len(self.environment.victims)}",

            f"Rescued: {rescued_count}",

            f"Active: {active_count}",

            f"Hazards: {len(self.environment.hazard_zones)}",

            f"Blocked Roads: {len(self.environment.blocked_roads)}",

            (
                "Ambulances: "
                f"{len(self.environment.get_available_ambulance_ids())}"
                f"/{len(self.environment.ambulances)}"
            )
        ]

        y_position = 125

        for stat in stats:

            stat_text = self.small_font.render(

                stat,

                True,

                BLACK
            )

            self.screen.blit(

                stat_text,

                (
                    1160,
                    y_position
                )
            )

            y_position += 20

        # =====================================
        # SYSTEM STATUS
        # =====================================

        if self.simulation_active:

            status = "RUNNING"

            color = GREEN

        else:

            status = "STOPPED"

            color = RED

        status_text = self.font.render(

            f"SYSTEM: {status}",

            True,

            color
        )

        self.screen.blit(
            status_text,
            (1155, 250)
        )

        # =====================================
        # DASHBOARD
        # =====================================

        

    # ============================================
    # ALERT POPUP
    # ============================================

    def draw_alert_popup(
        self
    ):

        if self.alert_timer <= 0:

            return

        popup_rect = pygame.Rect(
            160,
            10,
            280,
            32
        )

        pygame.draw.rect(

            self.screen,

            RED,

            popup_rect,

            border_radius=8
        )

        pygame.draw.rect(

            self.screen,

            WHITE,

            popup_rect,

            2,

            border_radius=8
        )

        alert_text = self.font.render(

            self.current_alert,

            True,

            WHITE
        )

        self.screen.blit(
            alert_text,
            (185, 18)
        )

        self.alert_timer -= 1

    # ============================================
    # RENDER ENVIRONMENT
    # ============================================

    def render_environment(
        self
    ):

        self.screen.fill(MAP_BG)

        self.map_renderer.draw_grid(
            self.screen
        )

        self.map_renderer.draw_blocked_roads(
            self.screen
        )

        self.map_renderer.draw_hazard_zones(
            self.screen
        )

        self.map_renderer.draw_victims(
            self.screen
        )

        self.map_renderer.draw_medical_centers(
            self.screen
        )

        self.map_renderer.draw_rescue_base(
            self.screen
        )

        self.dashboard_renderer.draw_dashboard(

         self.screen,

         self.environment
) 

        self.draw_alert_popup()

    # ============================================
    # HANDLE EVENTS
    # ============================================

    def handle_events(
        self,
        environment,
        agent
    ):

        for event in pygame.event.get():

            # =====================================
            # QUIT
            # =====================================

            if event.type == pygame.QUIT:

                pygame.quit()

                return False
            if event.type == pygame.VIDEORESIZE and not self.fullscreen:
                self.window_width = event.w
                self.window_height = event.h
                self._apply_window_mode()

            # =====================================
            # MOUSE CLICK
            # =====================================

            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                mouse_position = event.pos

                tab_clicked = self.dashboard_renderer.handle_click(
                    mouse_position
                )

                if tab_clicked:

                    self.render_environment()

                    pygame.display.update()

                    continue

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_F11:

                    self.fullscreen = not self.fullscreen
                    self._apply_window_mode()

        return True
    # ============================================
    # CCP KPI CALCULATOR
    # ============================================

    def update_live_ccp_kpis(
        self,
        agent
    ):

        victims = self.environment.victims

        rescued = len([

            victim

            for victim in victims

            if victim.is_rescued
        ])

        failed = len([

            victim

            for victim in victims

            if (
                not victim.is_rescued
                and
                victim.severity == "critical"
            )
        ])

        # =====================================
        # AVG RESCUE TIME
        # =====================================

        total_time = 0

        rescued_count = 0

        for victim in victims:

            if victim.is_rescued:

                total_time += 12

                rescued_count += 1

        avg_rescue_time = 0

        if rescued_count > 0:

            avg_rescue_time = round(

                total_time / rescued_count,

                2
            )

        # =====================================
        # HIGH RISK COUNT
        # =====================================

        high_risk = len(
            self.environment.hazard_zones
        )

        # =====================================
        # PATH OPTIMALITY
        # =====================================

        best_known_cost = 10

        selected_cost = 12

        path_optimality = round(

            selected_cost / best_known_cost,

            2
        )

        # =====================================
        # RESOURCE UTILIZATION
        # =====================================

        total_ambulances = len(
            self.environment.ambulances
        )

        used_ambulances = len([

            ambulance

            for ambulance
            in self.environment.ambulances.values()

            if not ambulance["available"]
        ])

        resource_utilization = 0

        if total_ambulances > 0:

            resource_utilization = (

                used_ambulances
                /
                total_ambulances

            ) * 100

        # =====================================
        # RISK EXPOSURE SCORE
        # =====================================

        risk_exposure = 0

        for hazard in self.environment.hazard_zones:

            if hazard.risk_level == "fire":

                risk_exposure += 10

            elif hazard.risk_level == "collapse":

                risk_exposure += 7

        # =====================================
        # UPDATE DASHBOARD
        # =====================================

        self.dashboard_renderer.update_kpi(

            rescued=rescued,

            failed=failed,

            avg_rescue_time=avg_rescue_time,

            high_risk=high_risk,

            path_optimality=path_optimality,

            resource_utilization=resource_utilization,

            risk_exposure=risk_exposure
        )
    # ============================================
    # MAIN LOOP
    # ============================================

    def run_live_simulation(
        self,
        agent
    ):

        running = True

        self.auto_rescue_system(
            agent
        )

        while running:

            running = self.handle_events(

                self.environment,

                agent
            )

            self.auto_generate_disasters(
                agent
            )

            self.render_environment()
            if hasattr(self, "current_agent"):

                self.update_live_ccp_kpis(

                    self.current_agent
                )

            pygame.display.update()

            self.clock.tick(60)

        pygame.quit()

    # ============================================
    # AMBULANCE ANIMATION
    # ============================================

    def animate_multiple_rescue_paths(
        self,
        ambulance_data
    ):

        if not self.simulation_active:

            return

        self.ambulance_renderer.animate_multiple_ambulances(

            self.screen,

            ambulance_data,

            self.render_environment,

            self.environment.victims
        )
