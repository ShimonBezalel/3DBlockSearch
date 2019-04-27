from copy import deepcopy

from stl import mesh

from dgrid import GRID_UNIT_WITH_SPACING
from orientation import orient_mesh

TARGET_MESH = mesh.Mesh.from_file("stl/target_cube.stl")
TARGET_WAITING_COLOR = "#FFFF11"
TARGET_REACHED_COLOR = "#22FF11"
TARGET_ALPHA = 0.8

class Target:
    def __init__(self, coordinates, color_waiting=TARGET_WAITING_COLOR, color_reached=TARGET_REACHED_COLOR, alpha=TARGET_ALPHA):
        self.position = tuple([int(GRID_UNIT_WITH_SPACING * cor) for cor in coordinates])
        self.mesh = deepcopy(TARGET_MESH)
        self.alpha = alpha
        self.color_waiting = color_waiting
        self.color_reached = color_reached
        orient_mesh(self.mesh, rotation=(0,0,0), translation=self.position)
        self.is_reached = False

    def get_mesh(self):
        return self.mesh

    def mark_as_reached(self):
        self.is_reached = True

    @property
    def color(self):
        if self.is_reached:
            return self.color_reached
        return self.color_waiting