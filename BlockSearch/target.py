from copy import deepcopy

from stl import mesh

import grid
from orientation import orient_mesh

TARGET_MESH = mesh.Mesh.from_file("stl/target_cube.stl")
TARGET_WAITING_COLOR = "#FFFF11"
TARGET_REACHED_COLOR = "#22FF11"
TARGET_HIGHLIGHT_COLOR = 'orange'
TARGET_ALPHA = 0.8


class Target:
    def __init__(self, coordinates, color_waiting=TARGET_WAITING_COLOR, color_reached=TARGET_REACHED_COLOR,
                 alpha=TARGET_ALPHA, color_highlight=TARGET_HIGHLIGHT_COLOR):
        self.position = tuple([int(grid.GRID_UNIT_WITH_SPACING * cor) for cor in coordinates])
        self.mesh = deepcopy(TARGET_MESH)
        self.alpha = alpha
        self.color_waiting = color_waiting
        self.color_reached = color_reached
        self.color_highlight = color_highlight
        orient_mesh(self.mesh, rotation=(0, 0, 0), translation=self.position)
        self.is_reached = False
        self.highlight = False

    def get_mesh(self):
        return self.mesh

    def mark_as_reached(self):
        self.is_reached = True

    def highlight_on(self):
        self.highlight = True

    def highlight_off(self):
        self.highlight = False

    @property
    def color(self):
        if self.is_reached:
            return self.color_reached
        if self.highlight:
            return self.color_highlight
        return self.color_waiting
