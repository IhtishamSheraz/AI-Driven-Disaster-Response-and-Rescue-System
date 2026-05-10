# ============================================
# File: visualization/path_renderer.py
# Description:
# Draw rescue paths on grid.
# ============================================

import pygame

from visualization.colors import *

from visualization.visualization_config import *


class PathRenderer:
    """
    Render selected rescue paths.
    """

    def draw_path(
        self,
        screen,
        path
    ):
        """
        Draw selected route path.
        """

        if len(path) < 2:

            return

        for index in range(
            len(path) - 1
        ):

            current_row, current_column = (
                path[index]
            )

            next_row, next_column = (
                path[index + 1]
            )

            start_x = (
                current_column
                *
                GRID_CELL_SIZE
                +
                GRID_CELL_SIZE // 2
            )

            start_y = (
                current_row
                *
                GRID_CELL_SIZE
                +
                GRID_CELL_SIZE // 2
            )

            end_x = (
                next_column
                *
                GRID_CELL_SIZE
                +
                GRID_CELL_SIZE // 2
            )

            end_y = (
                next_row
                *
                GRID_CELL_SIZE
                +
                GRID_CELL_SIZE // 2
            )

            pygame.draw.line(

                screen,

                PURPLE,

                (start_x, start_y),

                (end_x, end_y),

                4
            )