from BlockSearch.block import Block, ORIENTATIONS, ORIENTATION, Floor
from unittest import TestCase
from stl import mesh
from BlockSearch.render import *
from matplotlib.colors import to_rgba
import time

DISPLAY = True #False
block_mesh = mesh.Mesh.from_file('kapla.stl')
floor_mesh = mesh.Mesh.from_file('floor.stl')

class Tower_State_Test(TestCase):

    pass