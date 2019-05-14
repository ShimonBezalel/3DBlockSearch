from copy import copy

from BlockSearch.block import Block, ORIENTATIONS, ORIENTATION, Floor
from BlockSearch.tower_state import Tower_State
from unittest import TestCase
from stl import mesh
from BlockSearch.render import *
from matplotlib.colors import to_rgba
import time
from pprint import pprint as pp

DISPLAY = True #False
block_mesh = mesh.Mesh.from_file('kapla.stl')
floor_mesh = mesh.Mesh.from_file('floor.stl')

DISPLAY = True
TO_FILE = False

class Tower_State_Test(TestCase):
    def test_auto_close(self):
        block = Block(block_mesh, (0, 0, 0), (0, 0, 2))
        print("block created")
        display([b.render() for b in [block]], auto_close=True)


    def test_spread(self):
        tower_state = Tower_State()

        #same orientation
        orientation = 'tall_wide'
        block1 = Block(block_mesh, orientation, (0, 0, 0))
        block2 = Block(block_mesh, orientation, (2, 1, 0))

        spread = tower_state.get_spread(block1, block2)
        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread], scale=20)

        orientation = 'short_wide'
        block1 = Block(block_mesh, orientation, (0, 0, 0))
        block2 = Block(block_mesh, orientation, (5, 5, 0))

        spread = tower_state.get_spread(block1, block2)
        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread], scale=20)

        orientation = 'flat_thin'
        block1 = Block(block_mesh, orientation, ( 0,  0, 0))
        block2 = Block(block_mesh, orientation, (10, 10, 0))

        spread = tower_state.get_spread(block1, block2)
        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread], scale=20)

        # differing orientations - must have same top level
        block1 = Block(block_mesh, 'flat_wide', ( 0,  0, 0))
        block2 = Block(block_mesh, 'tall_thin', ( 5, 3, -7))

        spread = tower_state.get_spread(block1, block2)
        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread], scale=20)

        block1 = Block(block_mesh, 'flat_wide', ( 0,  0, 1))
        block2 = Block(block_mesh, 'short_thin', ( -10, 3, 0))

        spread = tower_state.get_spread(block1, block2)
        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread], scale=20)


        # test commutative quality of spread: ie. my spread with you is the same as yours spread with me.
        block1 = Block(block_mesh, 'flat_wide', ( 0,  0, 1))
        block2 = Block(block_mesh, 'short_thin', ( -15, 5, 0))

        spread1 = tower_state.get_spread(block1, block2)
        spread2 = tower_state.get_spread(block2, block1)

        self.assertEqual(spread1, spread2)

        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread1, spread2], scale=20)

        block1 = Block(block_mesh, (0, 0, 0), (0, 5, 1))
        block2 = Block(block_mesh, (0, 0, 0), (-2, -11, 1))
        block3 = Block(block_mesh, 'flat_wide', (-1, -6, 3))
        tower_state.set_blocks_above(block1, {block3})
        tower_state.set_blocks_above(block2, {block3})
        spread = tower_state.get_spread(block2, block1)

        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread], scale=20)

        block1 = Block(block_mesh, (0, 0, 0), (0, 9, 1))
        block2 = Block(block_mesh, (0, 0, 0), (-2, -13, 1))
        block3 = Block(block_mesh, 'flat_wide', (-1, -6, 3))
        tower_state.set_blocks_above(block1, {block3})
        tower_state.set_blocks_above(block2, {block3})
        spread = tower_state.get_spread(block2, block1)

        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread], scale=20)

        block1 = Block(block_mesh, 'short_thin', (-8, -1, 1))
        block2 = Block(block_mesh, 'short_thin', (7, 1, 1))
        block3 = Block(block_mesh, 'flat_wide', (0, 0, 3))
        tower_state.set_blocks_above(block1, {block3})
        tower_state.set_blocks_above(block2, {block3})
        spread = tower_state.get_spread(block2, block1)

        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread], scale=20)

    def test_tower_copy(self):
        tower1 = Tower_State()
        tower1_copy = copy(tower1)
        self.assertEqual(tower1, tower1_copy)
        self.assertTrue(tower1 is not tower1_copy)

        tower2 : Tower_State = Tower_State()
        for new_block in [Block(block_mesh, 'flat_wide', (0, 0, i)) for i in range(1, 50)]:
            if tower2.can_add(new_block):
                tower2.add(new_block)

        tower2_copy : Tower_State = copy(tower2)
        self.assertEqual(tower2, tower2_copy)
        self.assertTrue(tower2 is not tower2_copy)

        new_block = Block(block_mesh, 'flat_wide', (0, 0, 50))
        if tower2.can_add(new_block):
            tower2.add(new_block)
            print("Added new block to tower 2, {}".format(new_block.__str__()))

        self.assertNotEqual(tower2, tower2_copy)
        self.assertTrue(tower2 is not tower2_copy)

        self.assertNotEqual(tower2._connectivity, tower2_copy._connectivity)
        self.assertNotEqual(list(tower2._orientation_counter), list(tower2_copy._orientation_counter))

    def test_state_copy_time(self):
        results = dict()
        l = 6
        copies = dict()
        for t in range(10, 100, 20):
            tower : Tower_State = Tower_State()
            for new_block in [Block(block_mesh, 'flat_wide', (0, 0, i)) for i in range(1, t)]:
                if tower.can_add(new_block):
                    tower.add(new_block)

            s = time.time()
            copies[t] = [copy(tower) for _ in range(l)]
            e = time.time() - s
            results[t] = e / l
            print(results[t])
        pp(results)
        for height, tower_copy_list in copies.items():
            for i, tower in enumerate(tower_copy_list):
                new_block  = Block(block_mesh, 'flat_wide', (0, i, height))
                if tower.can_add(new_block):
                    tower.add(new_block)
        towers = []
        for copy_list in copies.values():
            towers += copy_list
        for i, tower1 in enumerate(towers):
            for j, tower2 in enumerate(towers[i+1:]):
                self.assertNotEqual(tower1, tower2)
                self.assertNotEqual(tower1._connectivity, tower2._connectivity)

    def test_iteration(self):
        tower: Tower_State = Tower_State()
        for new_block in [Block(block_mesh, 'flat_wide', (0, 0, i)) for i in range(1, 10)]:
            if tower.can_add(new_block):
                tower.add(new_block)

        for b in tower.gen_blocks():
            print(b.get_top_level())

    def test_covers(self):
        tower: Tower_State = Tower_State()
        for new_block in [Block(block_mesh, 'flat_wide', (0, 0, i)) for i in range(1, 10)]:
            if tower.can_add(new_block):
                tower.add(new_block)
        cover = tower.get_cover_at_level(0)
        for i in range(10):
            self.assertEqual(cover, tower.get_cover_at_level(i), str(tower.get_cover_at_level(i))+str(i))

        tower: Tower_State = Tower_State()
        for i in range(10):
            for j in range(i, 10 - i):
                new_block = Block(block_mesh, 'flat_thin', (0, j*3, i))
                if tower.can_add(new_block):
                    tower.add(new_block)
        if DISPLAY:
            display([b.render() for b in tower.gen_blocks()])
        prev = 10000
        for level in range(10):
            size = tower.get_cover_at_level(level).__len__()
            self.assertLessEqual(size, prev)
            prev = size

    def test_perp_tower(self):
        STAGE = 10
        tower: Tower_State = Tower_State(size=30, ring_floor=True)
        for i in range(100):
            added = []
            for father_block in tower.gen_blocks(no_floor=False):
                if not father_block.is_saturated(tower):
                    for son_desc in father_block.gen_possible_block_descriptors(
                            limit_orientation=lambda o: father_block.is_perpendicular(o), limit_len=STAGE / 2, random_order=True):
                        son_block = Block(floor_mesh, *son_desc)
                        if tower.can_add(son_block):
                            tower.add(son_block)
                            added.append(son_block)
                            if len(added) > STAGE:
                                break
                    if len(added) > STAGE:
                        break
            print(i)
            DISPLAY = False
            TO_FILE = True

            if DISPLAY or TO_FILE:
                old_meshes = [b.render() for b in filter(lambda b: b not in added, tower.gen_blocks())]
                new_meshes = [b.render() for b in added]
                display_colored(old_meshes + new_meshes,
                                ['gray'] * len(old_meshes) + ['cyan'] * len(new_meshes),
                                scale=60,
                                to_file=TO_FILE and not DISPLAY,
                                file_name="plots/ring_floor4/{0:03}.png".format(i)
                                )




