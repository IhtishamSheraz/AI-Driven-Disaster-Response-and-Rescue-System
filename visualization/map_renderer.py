# ============================================
# File: visualization/map_renderer.py
# Description:
# Responsible for rendering:
# - grid
# - victims
# - hazards
# - blocked roads
# - medical centers
# ============================================

import pygame

from visualization.colors import *

from visualization.visualization_config import *


class MapRenderer:
    """
    Render disaster environment.
    """

    def __init__(self, environment):

        self.environment = environment

        self.font = pygame.font.SysFont(
            "Arial",
            14,
            bold=True
        )

        self.small_font = pygame.font.SysFont(
            "Arial",
            10,
            bold=True
        )

    # ============================================
    # CELL RECT
    # ============================================

    def get_cell_rect(
        self,
        row,
        column,
        padding=4
    ):

        return pygame.Rect(

            column * GRID_CELL_SIZE + padding,
            row * GRID_CELL_SIZE + padding,
            GRID_CELL_SIZE - padding * 2,
            GRID_CELL_SIZE - padding * 2
        )

    # ============================================
    # CENTER LABEL
    # ============================================

    def draw_centered_text(
        self,
        screen,
        text,
        font,
        color,
        rect
    ):

        label = font.render(
            text,
            True,
            color
        )

        label_rect = label.get_rect(
            center=rect.center
        )

        screen.blit(
            label,
            label_rect
        )

    # ============================================
    # DRAW GRID
    # ============================================

    def draw_grid(self, screen):
        """
        Draw simulation grid.
        """

        for row in range(
            self.environment.rows
        ):

            for column in range(
                self.environment.columns
            ):

                rectangle = pygame.Rect(

                    column * GRID_CELL_SIZE,

                    row * GRID_CELL_SIZE,

                    GRID_CELL_SIZE,

                    GRID_CELL_SIZE
                )

                pygame.draw.rect(
                    screen,
                    ROAD_FILL,
                    rectangle
                )

                pygame.draw.rect(
                    screen,
                    GRID_LINE,
                    rectangle,
                    1
                )

    # ============================================
    # DRAW BLOCKED ROADS
    # ============================================

    def draw_blocked_roads(
        self,
        screen
    ):
        """
        Draw blocked road positions.
        """

        for row, column in (
            self.environment.blocked_roads
        ):

            rectangle = self.get_cell_rect(
                row,
                column
            )

            # =====================================
            # BLOCKED ROAD CELL
            # =====================================

            pygame.draw.rect(
                screen,
                (95, 104, 112),
                rectangle,
                border_radius=7
            )

            pygame.draw.line(
                screen,
                (132, 142, 150),
                rectangle.topleft,
                rectangle.bottomright,
                3
            )

            pygame.draw.line(
                screen,
                (132, 142, 150),
                rectangle.topright,
                rectangle.bottomleft,
                3
            )

            # =====================================
            # LABEL
            # =====================================

            self.draw_centered_text(
                screen,
                "BLOCK",
                self.small_font,
                WHITE,
                rectangle
            )

    # ============================================
    # DRAW HAZARD ZONES
    # ============================================

    def draw_hazard_zones(
        self,
        screen
    ):
        """
        Draw fire hazard zones.
        """

        for hazard in (
            self.environment.hazard_zones
        ):

            row, column = (
                hazard.location
            )

            rectangle = self.get_cell_rect(
                row,
                column
            )

            # =====================================
            # HAZARD CELL
            # =====================================

            if hazard.risk_level == "collapse":

                color = COLLAPSE_PURPLE
                label_text = "RISK"

            else:

                color = FIRE_RED
                label_text = "FIRE"

            pygame.draw.rect(
                screen,
                color,
                rectangle,
                border_radius=8
            )

            inner_rect = rectangle.inflate(
                -14,
                -14
            )

            pygame.draw.rect(
                screen,
                FIRE_ORANGE if label_text == "FIRE" else (187, 132, 255),
                inner_rect,
                2,
                border_radius=6
            )

            # =====================================
            # HAZARD LABEL
            # =====================================

            self.draw_centered_text(
                screen,
                label_text,
                self.font,
                WHITE,
                rectangle
            )

    # ============================================
    # DRAW VICTIMS
    # ============================================

    def draw_victims(
        self,
        screen
    ):
        """
        Draw victim locations.
        """

        for victim in (
            self.environment.victims
        ):

            row, column = (
                victim.location
            )

            center_x = (
                column * GRID_CELL_SIZE
                +
                GRID_CELL_SIZE // 2
            )

            center_y = (
                row * GRID_CELL_SIZE
                +
                GRID_CELL_SIZE // 2
            )

            # =====================================
            # RESCUED VICTIMS
            # =====================================

            if victim.is_rescued:

                color = HOSPITAL_GREEN

            # =====================================
            # CRITICAL
            # =====================================

            elif victim.severity == "critical":

                color = VICTIM_CRITICAL

            # =====================================
            # MODERATE
            # =====================================

            elif victim.severity == "moderate":

                color = VICTIM_MODERATE

            # =====================================
            # MINOR
            # =====================================

            else:

                color = VICTIM_MINOR

            # =====================================
            # DRAW VICTIM
            # =====================================

            pygame.draw.circle(

                screen,

                BLACK,

                (
                    center_x + 3,
                    center_y + 4
                ),

                18
            )

            pygame.draw.circle(

                screen,

                color,

                (
                    center_x,
                    center_y
                ),

                17
            )

            pygame.draw.circle(

                screen,

                WHITE,

                (
                    center_x,
                    center_y
                ),

                17,

                2
            )

            # =====================================
            # VICTIM LABEL
            # =====================================

            victim_label = self.font.render(

                f"V{victim.victim_id}",

                True,

                BLACK
            )

            screen.blit(

                victim_label,

                (
                    center_x - 10,
                    center_y - 8
                )
            )

            # =====================================
            # STATUS LABEL
            # =====================================

            if victim.is_rescued:

                status = "SAFE"

            elif victim.is_picked:

                status = "PICKED"

            else:

                status = victim.severity.upper()

            status_surface = self.small_font.render(

                status,

                True,

                WHITE
            )

            status_rect = status_surface.get_rect()
            status_rect.centerx = center_x
            status_rect.top = row * GRID_CELL_SIZE + 43

            badge_rect = status_rect.inflate(
                8,
                4
            )

            pygame.draw.rect(
                screen,
                PANEL_DARK,
                badge_rect,
                border_radius=4
            )

            screen.blit(

                status_surface,

                status_rect
            )

    # ============================================
    # DRAW MEDICAL CENTERS
    # ============================================

    def draw_medical_centers(
        self,
        screen
    ):
        """
        Draw medical center locations.
        """

        for row, column in (
            self.environment.medical_centers
        ):

            rectangle = self.get_cell_rect(
                row,
                column
            )

            pygame.draw.rect(
                screen,
                HOSPITAL_GREEN,
                rectangle,
                border_radius=8
            )

            pygame.draw.rect(
                screen,
                WHITE,
                rectangle,
                2,
                border_radius=8
            )

            self.draw_centered_text(
                screen,
                "HOSP",
                self.font,
                BLACK,
                rectangle
            )

    # ============================================
    # DRAW RESCUE BASE
    # ============================================

    def draw_rescue_base(
        self,
        screen
    ):
        """
        Draw rescue base.
        """

        row, column = (
            self.environment.rescue_base
        )

        rectangle = self.get_cell_rect(
            row,
            column
        )

        pygame.draw.rect(
            screen,
            BASE_BLUE,
            rectangle,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            WHITE,
            rectangle,
            2,
            border_radius=8
        )

        # =====================================
        # BASE LABEL
        # =====================================

        self.draw_centered_text(
            screen,
            "BASE",
            self.font,
            WHITE,
            rectangle
        )
