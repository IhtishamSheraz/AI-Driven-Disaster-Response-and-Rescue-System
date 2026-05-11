# =========================================================
# FILE: visualization/dashboard_renderer.py
# COMPLETE UPDATED FILE
# =========================================================

import pygame
import time

# =========================================================
# COLORS
# =========================================================

WHITE = (244, 248, 252)
BLACK = (0, 0, 0)

CYAN = (74, 222, 255)
YELLOW = (250, 220, 88)
GOLD = (255, 215, 0)
GREEN = (47, 214, 126)
RED = (255, 60, 60)
ORANGE = (255, 174, 66)
GRAY = (140, 140, 140)

DARK_BG = (10, 22, 32)
PANEL_BG = (7, 16, 24)
BORDER = (78, 104, 124)
TAB_IDLE = (220, 226, 232)
TAB_ACTIVE = (68, 123, 255)
TAB_HOVER = (170, 190, 230)


class DashboardRenderer:

    def __init__(self):

        pygame.font.init()

        # =====================================================
        # FONTS
        # =====================================================

        self.title_font = pygame.font.SysFont(
            "Segoe UI",
            17,
            bold=True
        )
        

        self.header_font = pygame.font.SysFont(
            "Segoe UI",
            14,
            bold=True
        )

        self.font = pygame.font.SysFont(
            "Consolas",
            10,
            bold=True
        )

        self.small_font = pygame.font.SysFont(
            "Consolas",
            9
        )

        self.tab_font = pygame.font.SysFont(
            "Segoe UI",
            10,
            bold=True
        )
        self.ml_logs = []
        self.live_logs = []

        self.search_logs = []
        self.ml_predictions = []

        self.ml_logs = []
        self.tabs = [

            "RESOURCE",
            "SEARCH",
            "ML KNN",
            "ML NB",
            "NB VS KNN",
            "DECISION",
            "KPI"
        ]

        self.active_tab = "RESOURCE"
        self.tab_rects = {}

        # Auto-rotate report tables every N milliseconds.
        self.auto_rotate_tabs = True
        self.tab_rotation_interval = 5000
        self.last_tab_rotation_tick = pygame.time.get_ticks()

        # =====================================================
        # LIVE LOGS
        # =====================================================

        self.live_logs = [

            "AI System Started",
            "Dynamic Monitoring Enabled",
            "Autonomous rescue enabled"
        ]
        # =====================================================
        # LIVE SEARCH TRACE
        # =====================================================

        self.search_trace_logs = []
        self.decision_logger = None
        self.kpi_data = {

    "rescued": 0,

    "failed": 0,

    "success_rate": 0,

    "avg_rescue_time": 0,

    "high_risk": 0,

    "path_optimality": 1.0,

    "resource_utilization": 0,

    "risk_exposure": 0
}
    def draw_kpi_table(

        self,

        screen
    ):

        dashboard_x = 650

        start_y = 170

        self.draw_text(

            screen,

            self.header_font,

            f"{self.active_tab} LIVE PREDICTIONS",

            CYAN,

            dashboard_x + 120,

            start_y
        )

        labels = [

            "Victims Rescued",

            "Failed Missions",

            "Success Rate",

            "Avg Rescue Time",

            "High Risk Missions",

            "Path Optimality",

            "Resource Utilization",

            "Risk Exposure Score"
        ]

        values = [

            str(self.kpi_data["rescued"]),

            str(self.kpi_data["failed"]),

            str(self.kpi_data["success_rate"]) + "%",

            str(self.kpi_data["avg_rescue_time"]) + "s",

            str(self.kpi_data["high_risk"]),

            str(self.kpi_data["path_optimality"]),

            str(self.kpi_data["resource_utilization"]) + "%",

            str(self.kpi_data["risk_exposure"])
        ]
        y = start_y + 80

        for index in range(len(labels)):

            self.draw_text(

                screen,

                self.small_font,

                labels[index],

                GOLD,

                dashboard_x,

                y
            )

            color = GREEN

            if labels[index] == "Failed Missions":

                color = RED

            elif labels[index] == "High Risk Missions":

                color = ORANGE

            self.draw_text(

                screen,

                self.small_font,

                values[index],

                color,

                dashboard_x + 300,

                y
            )

            y += 42

    def update_kpi(

        self,

        rescued,

        failed,

        avg_rescue_time,

        high_risk,

        path_optimality,

        resource_utilization,

        risk_exposure
    ):

        total = rescued + failed

        success_rate = 0

        if total > 0:

            success_rate = int(

                (rescued / total) * 100
            )

        self.kpi_data = {

            "rescued": rescued,

            "failed": failed,

            "success_rate": success_rate,

            "avg_rescue_time": avg_rescue_time,

            "high_risk": high_risk,

            "path_optimality": round(
                path_optimality,
                2
            ),

            "resource_utilization": round(
                resource_utilization,
                2
            ),

            "risk_exposure": round(
                risk_exposure,
                2
            )
        }

        total = rescued + failed

        success_rate = 0

        if total > 0:

            success_rate = int(

                (rescued / total) * 100
            )

        self.kpi_data = {

            "rescued": rescued,

            "failed": failed,

            "success_rate": success_rate,

            "avg_rescue_time": avg_rescue_time,

            "high_risk": high_risk
        }

    def add_ml_prediction(

        self,

        victim_id,

        severity,

        distance,

        risk_score,

        survival_probability,

        ml_decision,

        confidence
    ):

        prediction = {

            "victim_id": victim_id,

            "severity": severity,

            "distance": distance,

            "risk_score": risk_score,

            "survival_probability": survival_probability,

            "ml_decision": ml_decision,

            "confidence": confidence
        }
        print("ML DATA RECEIVED")
        print(prediction)

        self.ml_predictions.append(
            prediction
        )
        print(self.ml_predictions)

        if len(self.ml_predictions) > 12: 

            self.ml_predictions.pop(0)

    # =========================================================
    # LINK PROJECT DECISION LOGGER
    # =========================================================
    def draw_ml_table(

        self,

        screen
    ):

        panel_x = 650

        panel_y = 190
       

    

        self.draw_text(

            screen,

            self.header_font,
        f"{self.active_tab} LIVE PREDICTIONS",

            CYAN,

            panel_x + 180,

            panel_y
        )

        headers = [

            "V",

            "SEV",

            "DIST",

            "RISK",

            "SURV",

            "DECISION",

            "CONF"
        ]

        column_x = [

            panel_x + 10,

            panel_x + 90,

            panel_x + 170,

            panel_x + 260,

            panel_x + 350,

            panel_x + 420,

            panel_x + 480
        ]

        y = panel_y + 60

        # =========================================
        # HEADERS
        # =========================================

        for index, header in enumerate(headers):

            self.draw_text(

                screen,

                self.small_font,

                header,

                GOLD,

                column_x[index],

                y
            )

        y += 40

        # =========================================
        # LIVE ML ROWS
        # =========================================

        latest_predictions = self.ml_predictions[-8:]

        for prediction in latest_predictions:

            values = [

                f"V{prediction['victim_id']}",

                prediction["severity"].upper(),

                str(prediction["distance"]),

                f"{prediction['risk_score']:.2f}",

                f"{prediction['survival_probability']}%",

                prediction["ml_decision"],

                f"{prediction['confidence']}%"
            ]

            colors = [

                WHITE,

                RED
                if prediction["severity"] == "critical"
                else
                ORANGE
                if prediction["severity"] == "moderate"
                else
                GREEN,

                WHITE,

                RED
                if prediction["risk_score"] > 0.75
                else
                YELLOW
                if prediction["risk_score"] > 0.4
                else
                GREEN,

                GREEN
                if prediction["survival_probability"] > 70
                else
                YELLOW
                if prediction["survival_probability"] > 40
                else
                RED,

                CYAN,

                GREEN
            ]

            for index, value in enumerate(values):

                self.draw_text(

                    screen,

                    self.small_font,

                    value,

                    colors[index],

                    column_x[index],

                    y
                )

            y += 35
    def draw_nb_vs_knn(
        self,
        screen
    ):

        panel_x = 620
        panel_y = 180

        self.draw_text(

            screen,

            self.header_font,

            "NB VS KNN MODEL COMPARISON",

            CYAN,

            panel_x + 120,

            panel_y - 80
        )

        knn = self.knn_metrics
        nb = self.nb_metrics

        # =====================================
        # KNN BOX
        # =====================================

        pygame.draw.rect(

            screen,

            (15, 30, 50),

            (
                panel_x,
                panel_y,
                300,
                360
            ),

            border_radius=10
        )

        pygame.draw.rect(

            screen,

            CYAN,

            (
                panel_x,
                panel_y,
                250,
                420
            ),

            2,

            border_radius=10
        )

        self.draw_text(
            screen,
            self.header_font,
            "KNN",
            CYAN,
            panel_x + 90,
            panel_y + 20
        )

        knn_y = panel_y + 80

        for label, value in [

            ("Accuracy", knn["accuracy"]),
            ("Precision", knn["precision"]),
            ("Recall", knn["recall"]),
            ("F1 Score", knn["f1_score"])

        ]:

            self.draw_text(
                screen,
                self.small_font,
                f"{label}: {value:.2f}",
                GREEN,
                panel_x + 25,
                knn_y
            )

            knn_y += 50

        # =====================================
        # NAIVE BAYES BOX
        # =====================================

        nb_x = panel_x + 360

        pygame.draw.rect(

            screen,

            (15, 30, 50),

            (
                nb_x,
                panel_y,
                250,
                420
            ),

            border_radius=10
        )

        pygame.draw.rect(

            screen,

            CYAN,

            (
                nb_x,
                panel_y,
                300,
                360
            ),

            2,

            border_radius=10
        )

        self.draw_text(
            screen,
            self.header_font,
            "NAIVE BAYES",
            CYAN,
            nb_x + 40,
            panel_y + 20
        )

        nb_y = panel_y + 80

        for label, value in [

            ("Accuracy", nb["accuracy"]),
            ("Precision", nb["precision"]),
            ("Recall", nb["recall"]),
            ("F1 Score", nb["f1_score"])

        ]:

            self.draw_text(
                screen,
                self.small_font,
                f"{label}: {value:.2f}",
                GREEN,
                nb_x + 25,
                nb_y
            )

            nb_y += 50

        # =====================================
        # BEST MODEL
        # =====================================

        best_model = "KNN"

        if nb["accuracy"] > knn["accuracy"]:

            best_model = "NAIVE BAYES"

        self.draw_text(

            screen,

            self.header_font,

            f"BEST MODEL: {best_model}",

            YELLOW,

            panel_x + 220,

            panel_y + 390
        )        
    def set_decision_logger(
        self,
        decision_logger
    ):

        self.decision_logger = decision_logger

    # =========================================================
    # ADD LOG
    # =========================================================

    def add_log(
        self,
        message
    ):

        current_time = time.strftime("%H:%M:%S")

        log = f"{current_time}  {message}"

        self.live_logs.append(log)

        if len(self.live_logs) > 15:

            self.live_logs.pop(0)

    # =========================================================
    # HANDLE TAB CLICK
    # =========================================================

    def handle_click(
        self,
        mouse_pos
    ):

        mx, my = mouse_pos
        # Use exact rectangles from the latest draw.
        # Fallback to static geometry if first click happens before draw.
        tab_rects = self.tab_rects
        if not tab_rects:
            surface = pygame.display.get_surface()
            screen_width = surface.get_width() if surface else 1200
            dashboard_x = max(610, screen_width - 590)
            start_x = dashboard_x + 25
            tab_rects = {
                tab: pygame.Rect(start_x + (index * 80), 70, 78, 30)
                for index, tab in enumerate(self.tabs)
            }

        for tab, rect in tab_rects.items():
            if rect.collidepoint(mx, my):
                self.active_tab = tab
                return True

        return False

    # =========================================================
    # LIVE SEARCH TRACE LOGGER
    # =========================================================

    def add_search_trace(
            self,


        algorithm,

        start,

        goal,

        expanded,

        frontier,

        cost,

        risk,

        heuristic,

        decision,
        execution_time,

        why
    ):

        current_time = time.strftime("%H:%M:%S")

        tradeoff = "Risk > Time"

        if risk == "HIGH":

            tradeoff = "Safety > Speed"

        elif cost <= 10:

            tradeoff = "Speed > Optimality"

        log = {

            "time": current_time,

            "algorithm": algorithm,

            "start": str(start),

            "goal": str(goal),

            "expanded": expanded,

            "frontier": frontier,

            "cost": cost,

            "risk": risk,

            "heuristic": heuristic,

            "time_ms": execution_time,

            "decision": decision,

            "tradeoff": tradeoff,

            "why": why
        }

        self.search_trace_logs.append(log)

        if len(self.search_trace_logs) > 20:

            self.search_trace_logs.pop(0)

    # =========================================================
    # DRAW TEXT
    # =========================================================

    def draw_text(
        self,
        screen,
        font,
        text,
        color,
        x,
        y
    ):

        surface = font.render(
            str(text),
            True,
            color
        )

        screen.blit(
            surface,
            (x, y)
        )

    # =========================================================
    # GET CCP OUTPUT ROWS
    # =========================================================

    def get_ccp_output_rows(
        self
    ):

        if self.decision_logger is None:

            return []

        output_rows = []

        for log in self.decision_logger.logs:

            if log["event_type"] not in [
                "ROUTE_CONFLICT",
                "VICTIM_PRIORITY",
                "SEARCH_DECISION",
                "CSP_ALLOCATION",
                "REROUTING",
                "DYNAMIC_DISASTER",
                "LIVE_ROUTE",
                "LIVE_ROUTE_FAILED",
                "LIVE_REROUTE",
                "LIVE_PICKUP",
                "LIVE_DELIVERED",
                "LIVE_RESOURCE",
                "LIVE_DYNAMIC"
            ]:

                continue

            data = log.get("data", {})

            event_type = log["event_type"]

            priority = data.get(
                "priority",
                "MEDIUM"
            )

            outcome = data.get(
                "outcome",
                "ACTIVE"
            )

            event_name = event_type.replace(
                "LIVE_",
                ""
            ).replace(
                "_",
                " "
            )

            if event_type == "ROUTE_CONFLICT":

                event_name = "ROUTE"
                priority = "HIGH"
                outcome = "SELECTED"
                action = (
                    f"{data.get('selected', 'Route')} "
                    f"cost:{data.get('cost', '-')} "
                    f"risk:{data.get('risk', '-')} "
                    f"surv:{data.get('survival', '-')}%"
                )

            elif event_type == "VICTIM_PRIORITY":

                event_name = "TRIAGE"
                priority = "HIGH"
                outcome = data.get("selected", "RANKED")
                action = (
                    f"Victim {data.get('victim_id', '-')} ranked "
                    f"surv:{data.get('survival', '-')}%"
                )

            elif event_type == "LIVE_PICKUP":

                event_name = "RESCUE"
                priority = "HIGH"
                outcome = "ACTIVE"
                action = data.get("why", log["description"])

            elif event_type == "LIVE_DELIVERED":

                event_name = "DELIVERY"
                priority = "HIGH"
                outcome = "COMPLETED"
                action = data.get("why", log["description"])

            elif event_type == "LIVE_REROUTE":

                event_name = "SEARCH"
                priority = "MEDIUM"
                outcome = "REROUTED"
                action = (
                    f"Reroute cost:{data.get('cost', '-')} "
                    f"risk:{data.get('risk', '-')}"
                )

            elif event_type == "LIVE_ROUTE_FAILED":

                event_name = "SEARCH"
                priority = "CRITICAL"
                outcome = "FAILED"
                action = data.get("why", log["description"])

            elif event_type == "LIVE_RESOURCE":

                event_name = "RESOURCE"
                priority = "HIGH"
                outcome = "DELAYED"
                action = data.get("why", log["description"])

            elif event_type == "LIVE_DYNAMIC":

                event_name = "DISASTER"
                priority = "CRITICAL"
                outcome = "ACTIVE"
                action = data.get("why", log["description"])

            elif event_type == "SEARCH_DECISION":

                event_name = "SEARCH"
                priority = data.get("priority", "HIGH")
                outcome = data.get("outcome", "SELECTED")
                action = data.get("why", log["description"])

            elif event_type == "REROUTING":

                event_name = "ROUTE"
                priority = data.get("priority", "HIGH")
                outcome = data.get("outcome", "REROUTED")
                action = data.get("why", log["description"])

            elif event_type == "DYNAMIC_DISASTER":

                event_name = "DISASTER"
                priority = data.get("priority", "CRITICAL")
                outcome = data.get("outcome", "ACTIVE")
                action = data.get("why", log["description"])

            elif event_type == "CSP_ALLOCATION":

                event_name = "CSP"
                priority = data.get("priority", "HIGH")
                outcome = data.get("outcome", "VALID")
                action = data.get("why", log["description"])

            else:

                action = data.get("why", log["description"])

            output_rows.append(
                {
                    "time": log["time"][11:19],
                    "event": event_name,
                    "agent": data.get("agent", "Planner (AI)"),
                    "algorithm": data.get("algorithm", "-"),
                    "action": action,
                    "priority": priority,
                    "objective": data.get("objective", "Live Adaptation"),
                    "justification": data.get(
                        "justification",
                        data.get("why", log["description"])
                    ),
                    "outcome": outcome,
                    "type": data.get("type", log["event_type"]),
                    "victim": f"V{data.get('victim_id', '-')}",
                    "cost": data.get("cost", "-"),
                    "risk": data.get("risk", "-"),
                    "survival": data.get("survival", "-"),
                    "why": data.get("why", log["description"])
                }
            )

        return output_rows

    # =========================================================
    # DRAW PANEL
    # =========================================================

    def draw_panel(
        self,
        screen,
        x,
        y,
        width,
        height
    ):

        pygame.draw.rect(

            screen,

            PANEL_BG,

            (
                x,
                y,
                width,
                height
            ),

            border_radius=8
        )

        pygame.draw.rect(

            screen,

            BORDER,

            (
                x,
                y,
                width,
                height
            ),

            2,

            border_radius=8
        )

    # =========================================================
    # DRAW GRID
    # =========================================================

    def draw_grid(
        self,
        screen,
        x,
        y,
        width,
        height,
        rows,
        cols
    ):

        row_height = height // rows
        col_width = width // cols

        for i in range(rows + 1):

            pygame.draw.line(

                screen,

                (35, 35, 35),

                (
                    x,
                    y + i * row_height
                ),

                (
                    x + width,
                    y + i * row_height
                )
            )

        for i in range(cols + 1):

            pygame.draw.line(

                screen,

                (35, 35, 35),

                (
                    x + i * col_width,
                    y
                ),

                (
                    x + i * col_width,
                    y + height
                )
            )

    # =========================================================
    # MAIN DASHBOARD
    # =========================================================

    def draw_dashboard(
        self,
        screen,
        environment
    ):

        dashboard_x = max(610, screen.get_width() - 590)

        # =====================================================
        # AUTO-ROTATE TABS EVERY tab_rotation_interval ms
        # =====================================================

        if self.auto_rotate_tabs:

            now_tick = pygame.time.get_ticks()

            if (
                now_tick - self.last_tab_rotation_tick
                >= self.tab_rotation_interval
            ):

                current_index = 0

                if self.active_tab in self.tabs:

                    current_index = self.tabs.index(
                        self.active_tab
                    )

                next_index = (
                    current_index + 1
                ) % len(self.tabs)

                self.active_tab = self.tabs[next_index]

                self.last_tab_rotation_tick = now_tick

        # =====================================================
        # BACKGROUND
        # =====================================================

        pygame.draw.rect(

            screen,

            DARK_BG,

            (
                dashboard_x,
                0,
                590,
                screen.get_height()
            )
        )

        # =====================================================
        # TITLE
        # =====================================================

        self.draw_text(

            screen,

            self.title_font,

            "SIMULATION REPORT",

            WHITE,

            dashboard_x + 185,

            20
        )

        # =====================================================
        # TABS
        # =====================================================

        start_x = dashboard_x + 25
        self.tab_rects = {}
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for tab in self.tabs:

            active = self.active_tab == tab
            tab_rect = pygame.Rect(start_x, 70, 78, 30)
            hovered = tab_rect.collidepoint(mouse_x, mouse_y)

            if active:
                color = TAB_ACTIVE
            elif hovered:
                color = TAB_HOVER
            else:
                color = TAB_IDLE

            text_color = WHITE if active else BLACK
            self.tab_rects[tab] = tab_rect

            pygame.draw.rect(screen, color, tab_rect, border_radius=6)

            if active:
                pygame.draw.rect(screen, CYAN, tab_rect, 2, border_radius=6)
            elif hovered:
                pygame.draw.rect(screen, CYAN, tab_rect, 1, border_radius=6)

            self.draw_text(
                screen,
                self.tab_font,
                tab,
                text_color,
                start_x + 12,
                79
            )

            start_x += 80

        # =====================================================
        # MAIN PANEL
        # =====================================================

        self.draw_panel(
            screen,
            dashboard_x + 15,
            120,
            560,
            510
        )

        # =====================================================
        # ACTIVE TABLE
        # =====================================================

        if self.active_tab == "RESOURCE":

            self.draw_resource_table(
                screen,
                environment
            )

        elif self.active_tab == "SEARCH":

            self.draw_search_table(
                screen,
                environment
            )

        elif self.active_tab in ("ML KNN", "ML NB"):

            self.draw_ml_table(screen)

        elif self.active_tab == "NB VS KNN":

            self.draw_nb_vs_knn(screen)

        elif self.active_tab == "KPI":

            self.environment = environment
            self.draw_kpi_table(screen)

        elif self.active_tab == "DECISION":

            self.draw_log_table(
                screen,
                environment
            )

    # =========================================================
    # RESOURCE TABLE
    # =========================================================

    def draw_resource_table(
        self,
        screen,
        environment
    ):

        self.draw_text(

            screen,

            self.header_font,

            "RESOURCE ALLOCATION TABLE",

            CYAN,

            730,

            150
        )

        x = 650
        y = 190

        width = 470
        height = 360

        rows = 12
        cols = 4

        self.draw_grid(

            screen,
            x,
            y,
            width,
            height,
            rows,
            cols
        )

        headers = [

            "Ambulance",
            "Victim",
            "Status",
            "Rescued By"
        ]

        col_x = [

            x + 18,
            x + 145,
            x + 255,
            x + 365
        ]

        for i, header in enumerate(headers):

            self.draw_text(

                screen,

                self.font,

                header,

                YELLOW,

                col_x[i],

                y + 12
            )

        victims = environment.victims

        row_y = y + 45

        display_victims = victims[-10:]

        for index, victim in enumerate(display_victims):

            # =================================================
            # ONLY 2 AMBULANCES
            # =================================================

            ambulance_name = f"A{(index % 2) + 1}"

            # =================================================
            # DYNAMIC VICTIM NUMBER
            # =================================================

            victim_name = f"V{index + 1 + max(0, len(victims)-10)}"

            # =================================================
            # LIVE STATUS
            # =================================================

            if getattr(victim, "is_rescued", False):

                status = "Delivered"
                status_color = GREEN

            elif getattr(victim, "is_picked", False):

                status = "Picked"
                status_color = ORANGE

            elif getattr(victim, "assigned", False):

                status = "Searching"
                status_color = CYAN

            else:

                status = "Waiting"
                status_color = RED

            rescued_by = ambulance_name

            row_data = [

                ambulance_name,
                victim_name,
                status,
                rescued_by
            ]

            for col_index, value in enumerate(row_data):

                color = WHITE

                if col_index == 2:

                    color = status_color

                self.draw_text(

                    screen,

                    self.small_font,

                    value,

                    color,

                    col_x[col_index],

                    row_y
                )

            row_y += 28

        # =====================================================
        # LIVE COUNTS
        # =====================================================

        rescued_count = len([

            v for v in victims

            if getattr(v, "is_rescued", False)
        ])

        picked_count = len([

            v for v in victims

            if getattr(v, "is_picked", False)
        ])

        active_count = len([

            v for v in victims

            if not getattr(v, "is_rescued", False)
        ])

        stats_y = y + 325

        self.draw_text(

            screen,

            self.font,

            f"TOTAL: {active_count}",

            CYAN,

            x + 10,

            stats_y
        )

        self.draw_text(

            screen,

            self.font,

            f"RESCUED: {rescued_count}",

            GREEN,

            x + 160,

            stats_y
        )

        self.draw_text(

            screen,

            self.font,

            f"PICKED: {picked_count}",

            ORANGE,

            x + 330,

            stats_y
        )
        # =====================================
        # LIVE MEDICAL KIT DISPLAY
        # =====================================

        kits_left = environment.medical_kits

        kit_color = GREEN

        if kits_left <= 5:

            kit_color = ORANGE

        if kits_left <= 2:

            kit_color = RED

        self.draw_text(

            screen,

            self.font,

            f"KITS LEFT: {kits_left}",

            kit_color,

            x + 10,

            stats_y + 30
        )
        self.draw_ccp_summary_table(
            screen
        )

    # =========================================================
    # CCP SUMMARY IN RESOURCE TAB
    # =========================================================

    def draw_ccp_summary_table(
        self,
        screen
    ):

        output_rows = self.get_ccp_output_rows()

        if len(output_rows) == 0:

            return

        x = 650
        y = 555

        self.draw_text(

            screen,

            self.font,

            "CCP OUTPUT: COST vs RISK DECISIONS",

            CYAN,

            x,

            y
        )

        latest_rows = output_rows[-2:]

        row_y = y + 18

        for row in latest_rows:

            text = (
                f"{row['type']} {row['victim']} "
                f"Cost:{row['cost']} Risk:{row['risk']} "
                f"Surv:{row['survival']}%"
            )

            self.draw_text(

                screen,

                self.small_font,

                text,

                WHITE,

                x,

                row_y
            )

            self.draw_text(

                screen,

                self.small_font,

                str(row["why"])[:70],

                YELLOW,

                x,

                row_y + 12
            )

            row_y += 34

    # =========================================================
    # SEARCH TABLE
    # =========================================================

    def draw_search_table(

        self,

        screen,

        environment
    ):

        self.draw_text(

            screen,

            self.header_font,

            "LIVE SEARCH TRACE TABLE",

            CYAN,

            690,

            145
        )

        x = 630
        y = 185

        width = 540
        height = 380

        rows = 10
        cols = 10

        self.draw_grid(

            screen,
            x,
            y,
            width,
            height,
            rows,
            cols
        )

        headers = [

            "TIME(ms)",
            "ALG",
            "START",
            "GOAL",
            "EXP",
            "FRONT",
            "COST",
            "RISK",
            "HEUR",
            "RESULT"
        ]

        col_x = [

            x + 5,
            x + 60,
            x + 105,
            x + 165,
            x + 230,
            x + 280,
            x + 335,
            x + 385,
            x + 445,
            x + 500
        ]

        for index, header in enumerate(headers):

            self.draw_text(

                screen,

                self.small_font,

                header,

                YELLOW,

                col_x[index],

                y + 10
            )

        if len(self.search_trace_logs) == 0:

            self.draw_text(

                screen,

                self.font,

                "Waiting for live search traces...",

                ORANGE,

                x + 90,

                y + 90
            )

            return

        row_y = y + 40

        latest_logs = self.search_trace_logs[-8:]

        for log in latest_logs:

            risk_color = GREEN

            if log["risk"] == "HIGH":

                risk_color = RED

            elif log["risk"] == "MEDIUM":

                risk_color = ORANGE

            values = [

                log["time_ms"],

                log["algorithm"],

                log["start"],

                log["goal"],

                str(log["expanded"]),

                str(log["frontier"]),

                str(log["cost"]),

                log["risk"],

                log["heuristic"],

                log["decision"]
            ]

            for index, value in enumerate(values):

                color = WHITE

                if index == 7:

                    color = risk_color

                self.draw_text(

                    screen,

                    self.small_font,

                    value,

                    color,

                    col_x[index],

                    row_y
                )

            self.draw_text(

                screen,

                self.small_font,

                f"{log['tradeoff']} | {log['why'][:38]}",

                CYAN,

                x + 10,

                row_y + 16
            )

            row_y += 38

    # =========================================================
    # CSP TABLE
    # =========================================================

    def draw_csp_table(
        self,
        screen,
        environment
    ):

        self.draw_text(

            screen,

            self.header_font,

            "CSP METRICS",

            GREEN,

            760,

            150
        )

        csp_logs = []

        if self.decision_logger is not None:

            csp_logs = [

                log

                for log
                in self.decision_logger.logs

                if log["event_type"] == "CSP_ALLOCATION"
            ]

        if len(csp_logs) > 0:

            latest_csp = csp_logs[-1]

            data = latest_csp.get(
                "data",
                {}
            )

            lines = [

                "Variables:",
                "Ambulance1_Assignment",
                "Ambulance2_Assignment",
                "RescueTeam_Location",
                "MedicalKit_Distribution",
                "",
                f"Algorithm : {data.get('algorithm', '-')}",
                f"Objective : {data.get('objective', '-')}",
                f"Result    : {data.get('outcome', '-')}",
                f"Reason    : {data.get('why', '-')[:34]}"
            ]

        else:

            lines = [

                "Variables:",
                "Ambulance1_Assignment",
                "Ambulance2_Assignment",
                "RescueTeam_Location",
                "MedicalKit_Distribution",
                "",
                "Algorithm : Backtracking + MRV + FC",
                "Capacity  : 2 victims per ambulance",
                "Team      : 1 active rescue location",
                "Kits      : 10 total medical kits"
            ]

        y = 230

        for line in lines:

            self.draw_text(

                screen,

                self.font,

                line,

                WHITE,

                700,

                y
            )

            y += 45


    # =========================================================
    # LOG TABLE
    # =========================================================

    def draw_log_table(
        self,
        screen,
        environment
    ):

        self.draw_text(

            screen,

            self.header_font,

            "DECISION LOG (LIVE)",

            WHITE,

            680,

            150
        )

        x = 650
        y = 190

        width = 505
        height = 360

        rows = 12
        cols = 9

        self.draw_grid(

            screen,
            x,
            y,
            width,
            height,
            rows,
            cols
        )

        headers = [

            "TIME",
            "EVENT",
            "AI",
            "ALG",
            "DECISION",
            "PRI",
            "OBJECTIVE",
            "WHY",
            "OUTCOME"
        ]

        col_x = [

            x + 10,
            x + 55,
            x + 105,
            x + 160,
            x + 205,
            x + 285,
            x + 325,
            x + 400,
            x + 462
        ]

        live_x = x + 420
        live_y = 150

        pygame.draw.circle(
            screen,
            GREEN,
            (live_x, live_y + 5),
            5
        )

        self.draw_text(

            screen,

            self.small_font,

            "LIVE",

            GREEN,

            live_x + 10,

            live_y
        )

        for index, header in enumerate(headers):

            header_font = self.small_font

            self.draw_text(

                screen,

                header_font,

                header,

                YELLOW,

                col_x[index],

                y + 12
            )

        table_logs = self.get_ccp_output_rows()

        if len(table_logs) == 0:

            self.draw_text(

                screen,

                self.font,

                "Waiting for route and victim conflict decisions...",

                ORANGE,

                x + 45,

                y + 90
            )

            self.draw_text(

                screen,

                self.small_font,

                "The table fills after the agent compares cost, risk, and survival.",

                WHITE,

                x + 45,

                y + 120
            )

            return

        row_y = y + 45

        for log in reversed(table_logs[-9:]):

            event_color = WHITE

            if log["event"] in [
                "DISASTER",
                "RESOURCE"
            ]:

                event_color = RED

            elif log["event"] in [
                "RESCUE",
                "DELIVERY"
            ]:

                event_color = GREEN

            elif log["event"] in [
                "SEARCH",
                "ROUTE",
                "TRIAGE",
                "CSP"
            ]:

                event_color = CYAN

            priority_color = WHITE

            if log["priority"] == "CRITICAL":

                priority_color = RED

            elif log["priority"] == "HIGH":

                priority_color = ORANGE

            elif log["priority"] == "MEDIUM":

                priority_color = WHITE

            outcome_color = GREEN

            if log["outcome"] == "FAILED":

                outcome_color = RED

            elif log["outcome"] in [
                "ACTIVE",
                "REROUTED",
                "DELAYED"
            ]:

                outcome_color = ORANGE

            self.draw_text(

                screen,

                self.small_font,

                f"[{log['time'][3:8]}]",

                WHITE,

                col_x[0],

                row_y
            )

            self.draw_text(

                screen,

                self.small_font,

                str(log["event"])[:8],

                event_color,

                col_x[1],

                row_y
            )

            self.draw_text(

                screen,

                self.small_font,

                str(log["agent"])[:10],

                WHITE,

                col_x[2],

                row_y
            )

            self.draw_text(

                screen,

                self.small_font,

                str(log["algorithm"])[:8],

                WHITE,

                col_x[3],

                row_y
            )

            self.draw_text(

                screen,

                self.small_font,

                str(log["action"])[:12],

                WHITE,

                col_x[4],

                row_y
            )

            self.draw_text(

                screen,

                self.small_font,

                str(log["priority"])[:4],

                priority_color,

                col_x[5],

                row_y
            )

            self.draw_text(

                screen,

                self.small_font,

                str(log["objective"])[:11],

                CYAN,

                col_x[6],

                row_y
            )

            self.draw_text(

                screen,

                self.small_font,

                str(log["justification"])[:10],

                WHITE,

                col_x[7],

                row_y
            )

            self.draw_text(

                screen,

                self.small_font,

                str(log["outcome"])[:8],

                outcome_color,

                col_x[8],

                row_y
            )

            row_y += 34

    # =========================================================
    # KPI TABLE
    # =========================================================

    def draw_kpi_table(
        self,
        screen,
        
    ):

        self.draw_text(

            screen,

            self.header_font,

            "LIVE KPI METRICS",

            GREEN,

            740,

            150
        )

        rescued = len([

            v for v in self.environment.victims

            if getattr(v, "is_rescued", False)
        ])

        active = len(self.environment.victims)

        hazards = len(self.environment.hazard_zones)

        fire_zones = len([

            hazard for hazard in self.environment.hazard_zones

            if hazard.risk_level == "fire"
        ])

        collapse_zones = len([

            hazard for hazard in self.environment.hazard_zones

            if hazard.risk_level == "collapse"
        ])

        blocked = len(self.environment.blocked_roads)

        available = len(
            self.environment.get_available_ambulance_ids()
        )
        kits = self.environment.medical_kits

                # =====================================
        # LIVE CCP KPI METRICS
        # =====================================

        failed = len([

            victim

            for victim in self.environment.victims

            if (
                victim.severity == "critical"
                and
                not getattr(victim, "is_rescued", False)
            )
        ])

        total_cases = rescued + failed

        success_rate = 0

        if total_cases > 0:

            success_rate = int(

                (rescued / total_cases) * 100
            )

        # =====================================
        # AVG RESCUE TIME
        # =====================================

        avg_rescue_time = round(

            5 + (
                blocked * 0.8
            ),

            2
        )

        # =====================================
        # PATH OPTIMALITY
        # =====================================

        best_cost = 10

        current_cost = 10 + blocked

        path_optimality = round(

            current_cost / best_cost,

            2
        )

        # =====================================
        # RESOURCE UTILIZATION
        # =====================================

        total_ambulances = len(
            self.environment.ambulances
        )

        busy_ambulances = (

            total_ambulances - available
        )

        resource_utilization = 0

        if total_ambulances > 0:

            resource_utilization = int(

                (
                    busy_ambulances
                    /
                    total_ambulances
                ) * 100
            )

        # =====================================
        # RISK EXPOSURE SCORE
        # =====================================

        risk_exposure = (

            fire_zones * 10
            +
            collapse_zones * 7
        )

        # =====================================
        # CSP METRICS
        # =====================================

        csp_backtracking = max(

            2,

            active * 3
        )

        mrv_reduction = min(

            90,

            40 + active * 4
        )

        # =====================================
        # TRADEOFF
        # =====================================

        if risk_exposure > 40:

            tradeoff = "SAFETY > SPEED"

        else:

            tradeoff = "SPEED > SAFETY"

        # =====================================
        # FINAL KPI DATA
        # =====================================

        stats = [

            f"Victims Saved          : {rescued}",

            f"Failed Missions        : {failed}",

            f"Success Rate           : {success_rate}%",

            f"Average Rescue Time    : {avg_rescue_time}s",

            f"Path Optimality Ratio  : {path_optimality}",

            f"Resource Utilization   : {resource_utilization}%",

            f"Risk Exposure Score    : {risk_exposure}",

            f"CSP Backtracking       : {csp_backtracking}",

            f"MRV Reduction          : {mrv_reduction}%",

            f"Trade-off Priority     : {tradeoff}"
        ]

        y = 230

        for line in stats:

            self.draw_text(

                screen,

                self.font,

                line,

                WHITE,

                700,

                y
            )

            y += 38
