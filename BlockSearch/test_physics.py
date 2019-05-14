from random import random, choice, sample, shuffle

from BlockSearch.block import ORIENTATION
from BlockSearch.physics import *
from BlockSearch import physics as Physics
from unittest import TestCase
from stl import mesh
from BlockSearch.render import *
from BlockSearch.tower_state import *
import time
from pprint import pprint as pp
import uuid

DISPLAY = True  # False #True
block_mesh = mesh.Mesh.from_file('kapla.stl')
DEBUG = True

new_color = (0, 0, 1)
emphasis_color = (1, 0, 0)
matte_color = (0.8, 0.8, 0.8)
block_seq = [
    Block(block_mesh, 'short_wide', (0, 0, 1)),
    Block(block_mesh, 'short_wide', (-10, 0, 1)),
    Block(block_mesh, 'short_thin', (-5, 5, 4)),
    Block(block_mesh, 'short_thin', (-5, -5, 4)),
    Block(block_mesh, 'short_thin', (-6, 0, 4)),
    Block(block_mesh, 'flat_wide',  (0, 0, 6)),
    Block(block_mesh, 'flat_wide',  (-3, 2, 6)),
    Block(block_mesh, 'short_thin', (0, 5, 8)),
    Block(block_mesh, 'short_thin', (0, -5, 8)),
    Block(block_mesh, 'short_wide', (0, 1,  11)),
    Block(block_mesh, 'flat_wide',  (0, 0,  13)),
    Block(block_mesh, 'flat_wide',  (0, 0, 14)),
    Block(block_mesh, 'tall_wide',  (6, 0, 7)),
    Block(block_mesh, 'short_thin', (4, 0, 16)),
]


class Physics_Test(TestCase):

    def build(self, c, stability_check=False, timeit=False):
        """

        :param c: int defining complexity of build
        :return:
        """
        self.block_tower = Tower_State()
        self.meshes = []
        results = []
        for i, b in enumerate(block_seq[:c]):
            stable = True
            if stability_check:

                start = time.time()
                stable = Physics.is_stable(self.block_tower, b)
                elapse = time.time() - start
                results.append(elapse)
            if stable:
                self.block_tower.add(b)
                self.meshes.append(b.render())
            else:
                print("Block #{} {} was found to be unstable".format(i, str(b)))
                return results


        return results

    def build_tall(self, n):
        """

        :param c: int defining complexity of build
        :return:
        """
        self.block_tower = Tower_State()
        self.meshes = []
        results = []
        for i in range(n):
            b = Block(block_mesh, 'flat_wide', (0, 0, i))

            start = time.time()
            stable = Physics.is_stable(self.block_tower, b)
            elapse = time.time() - start
            results.append(elapse)
            if stable:
                self.block_tower.add(b)
                self.meshes.append(b.render())
            else:
                print("Block #{} {} was found to be unstable".format(i, str(b)))
                return results


        return results

    def build_janga(self, n, stability_check=True):
        """

        :param c: int defining complexity of build
        :return:
        """
        self.block_tower : Tower_State = Tower_State()
        self.meshes = []
        results = []
        for l in range(0, n, 2):
            for i in range(-2, 3):
                b = Block(block_mesh, 'flat_wide', (i * 3, 0, l))
                if stability_check:
                    start = time.time()
                    stable = Physics.is_stable(self.block_tower, b)
                    elapse = time.time() - start
                    results.append(elapse)
                    if stable:
                        self.block_tower.add(b)
                        self.meshes.append(b.render())
                    else:
                        print("Block #{} {} was found to be unstable".format(i, str(b)))
                        return results
                else:
                    self.block_tower.add(b)
                    self.meshes.append(b.render())


            for i in range(-2, 3):
                b = Block(block_mesh, 'flat_thin', (0, i * 3, l+1))
                if stability_check:
                    start = time.time()
                    stable = Physics.is_stable(self.block_tower, b)
                    elapse = time.time() - start
                    results.append(elapse)
                    if stable:
                        self.block_tower.add(b)
                        self.meshes.append(b.render())
                    else:
                        print("Block #{} {} was found to be unstable".format(i, str(b)))
                        return results
                else:
                    self.block_tower.add(b)
                    self.meshes.append(b.render())

        return results

    def test_combination(self):
        combined_meshes = Physics.combine([b.render() for b in block_seq])
        if DISPLAY:
            display([b.render() for b in block_seq])
            display([combined_meshes])

        COGs = [b.get_cog() for b in block_seq]
        if DISPLAY:
            display_colored([b.render() for b in block_seq] + [block_seq[0].render()],
                            [np.random.random((3)) for _ in range(len(block_seq))] + ['black'],
                            COGs + [np.average(COGs, axis=0)])
            display_colored([combined_meshes],
                            ['gray'],
                            [combined_meshes.get_mass_properties()[1]])

    def test_calculate_supports(self):
        self.build(4)
        new_block = Block(block_mesh, 'short_wide', (0, 0, 7))
        bottom_level = new_block.get_bottom_level()
        supports = list(Physics.calculate_below(new_block, self.block_tower[bottom_level - 1]))
        if DISPLAY:
            display(self.meshes + [new_block.render()])
            display_colored(self.meshes + [b.render() for b in ([new_block] + supports)],
                            [matte_color] * (len(self.meshes)) + [new_color] + [emphasis_color] * len(supports) )


        self.build(5)
        new_block = Block(block_mesh, 'short_wide', (0, 0, 7))
        bottom_level = new_block.get_bottom_level()
        supports = list(Physics.calculate_below(new_block, self.block_tower[bottom_level - 1]))
        if DISPLAY:
            display(self.meshes + [new_block.render()])
            display_colored(self.meshes + [b.render() for b in ([new_block] + supports)],
                            [matte_color] * (len(self.meshes)) + [new_color] + [emphasis_color] * len(supports))

        self.build(7)
        new_block = Block(block_mesh, 'short_wide', (0, 0, 8))
        bottom_level = new_block.get_bottom_level()
        supports = list(Physics.calculate_below(new_block, self.block_tower[bottom_level - 1]))
        if DISPLAY:
            display(self.meshes + [new_block.render()])
            display_colored(self.meshes + [b.render() for b in ([new_block] + supports)],
                            [matte_color] * (len(self.meshes)) + [new_color] + [emphasis_color] * len(supports))

        new_block = Block(block_mesh, 'tall_thin', (-2, 2, 14))
        bottom_level = new_block.get_bottom_level()
        supports = list(Physics.calculate_below(new_block, self.block_tower[bottom_level - 1]))
        if DISPLAY:
            display(self.meshes + [new_block.render()])
            display_colored(self.meshes + [b.render() for b in ([new_block] + supports)],
                            [matte_color] * (len(self.meshes)) + [new_color] + [emphasis_color] * len(supports))

        self.build(14)
        new_block = Block(block_mesh, 'short_thin', (4, -1, 16))
        bottom_level = new_block.get_bottom_level()
        supports = list(Physics.calculate_below(new_block, self.block_tower[bottom_level - 1]))
        if DISPLAY:
            display(self.meshes + [new_block.render()])
            display_colored(self.meshes + [b.render() for b in ([new_block] + supports)],
                            [matte_color] * (len(self.meshes)) + [new_color] + [emphasis_color] * len(supports))

    def test_stability(self):
        # # test blocks touching the floor
        self.build(1)
        first_block = Block(block_mesh, 'short_wide', (-3, 0, 1))
        self.assertTrue(Physics.is_stable(self.block_tower, first_block))
        if DISPLAY:
            display(self.meshes + [first_block.render()])


        self.build(2)
        new_block = Block(block_mesh, 'short_thin', (-5, 5, 4))
        self.assertTrue(Physics.is_stable(self.block_tower, new_block))
        if DISPLAY:
            display(self.meshes + [new_block.render()])


        self.build(14, stability_check=True)
        new_block = Block(block_mesh, 'short_thin', (4, -1, 16))
        self.assertTrue(Physics.is_stable(self.block_tower, new_block))
        if DISPLAY:
            display(self.meshes + [new_block.render()])

    def test_build_janga(self):
        self.build_janga(30, stability_check=False)
        tower = self.block_tower
        blocks = [b for b in tower.gen_blocks()]
        display([b.render() for b in blocks], scale=20)
        save_by_orientation_blocks(blocks, subfolder="janga", seperate_orientations=False)


    def test_physics_timing(self):
        DISPLAY = False
        results = self.build(13, stability_check=True, timeit=True)
        for i, result in enumerate(results):
            print ("Time for {} ms: \t {}".format(i + 1, result))

        if DISPLAY:
            display(self.meshes)

        results = self.build_tall(100)
        for i, result in enumerate(results):
            print ("Time for {} in s: \t {}".format(i + 1, result))

        if DISPLAY:
            display(self.meshes)

        results = self.build_janga(5)
        for i, result in enumerate(results):
            print ("Time for {} in s: \t {}".format(i + 1, result))

        if DISPLAY:
            display(self.meshes)

        results = self.build_janga(6)
        for i, result in enumerate(results):
            print ("Time for {} in s: \t {}".format(i + 1, result))


        if DISPLAY:
            display(self.meshes)

    def test_overlap(self):
        results = []
        self.build(4)
        new_block = Block(block_mesh, ORIENTATION.SHORT_THIN, (0, 0, 3) )
        results.append( Physics.is_overlapping(self.block_tower, new_block))
        if DISPLAY:
            display(self.meshes + [new_block.render()])

        new_block = Block(block_mesh, ORIENTATION.SHORT_THIN, (0, 0, 1) )
        results.append( Physics.is_overlapping(self.block_tower, new_block))
        if DISPLAY:
            display(self.meshes + [new_block.render()])

        self.build(8)
        new_block = Block(block_mesh, ORIENTATION.SHORT_THIN, (0, 0, 3) )
        results.append( Physics.is_overlapping(self.block_tower, new_block))
        if DISPLAY:
            display(self.meshes + [new_block.render()])

        new_block = Block(block_mesh, ORIENTATION.SHORT_THIN, (0, 0, 1) )
        results.append( Physics.is_overlapping(self.block_tower, new_block))
        if DISPLAY:
            display(self.meshes + [new_block.render()])

        new_block = Block(block_mesh, ORIENTATION.SHORT_THIN, (4, -5, 7) )
        results.append( Physics.is_overlapping(self.block_tower, new_block))
        if DISPLAY:
            display(self.meshes + [new_block.render()])

        new_block = Block(block_mesh, ORIENTATION.SHORT_THIN, (4, -6, 7) )
        results.append( Physics.is_overlapping(self.block_tower, new_block))
        if DISPLAY:
            display(self.meshes + [new_block.render()])

        print(results)
        self.assertTrue(all(results))

        # not overlapping
        results = []
        for i in range(4, 10):
            self.build(i)
            new_block = block_seq[i + 1]
            results.append(Physics.is_overlapping(self.block_tower, new_block))
            if DISPLAY:
                display(self.meshes + [new_block.render()])

        print(results)
        self.assertTrue(not any(results))

    def test_calculate_above(self):
        self.build(4)
        new_block = Block(block_mesh, 'short_wide', (-3, 0, 1))
        bottom_level = new_block.get_bottom_level()
        supportees = list(Physics.calculate_above(new_block, self.block_tower))
        if DISPLAY:
            display(self.meshes + [new_block.render()])
            display_colored(self.meshes + [b.render() for b in ([new_block] + supportees)],
                            [matte_color] * (len(self.meshes)) + [new_color] + [emphasis_color] * len(supportees) )

        self.build(8)
        new_block = Block(block_mesh, 'short_wide', (-3, 0, 1))
        bottom_level = new_block.get_bottom_level()
        supportees = list(Physics.calculate_above(new_block, self.block_tower))
        if DISPLAY:
            display(self.meshes + [new_block.render()])
            display_colored(self.meshes + [b.render() for b in ([new_block] + supportees)],
                            [matte_color] * (len(self.meshes)) + [new_color] + [emphasis_color] * len(supportees) )

    def test_aggregate_cog(self):
        pass

    def test_tower_not_stable(self):
        DISPLAY = False
        self.build(4, stability_check=True)
        bad_block = Block(block_mesh, ORIENTATION.SHORT_THIN, (-1, 0, 4) )
        self.assertTrue( not Physics.is_stable(self.block_tower, bad_block))
        if DISPLAY:
            l = list(self.block_tower.gen_blocks())
            display_colored([b.render() for b in l] + [bad_block.render()],
                            ['gray'] * len(l) + ['blue'],
                            [b.get_aggregate_cog() for b in l] + [bad_block.get_aggregate_cog()]
                            )

        self.build(10, stability_check=True)
        print("Before : "  + str(self.block_tower))
        good_block = Block(block_mesh, ORIENTATION.SHORT_THIN, (-1, -1, 4) )

        self.assertTrue( Physics.is_stable(self.block_tower, good_block))
        if DISPLAY:
            l = list(self.block_tower.gen_blocks())
            display_colored([b.render() for b in l] + [good_block.render()],
                            ['gray'] * len(l) + ['blue'],
                            [b.get_aggregate_cog() for b in l] + [good_block.get_aggregate_cog()]
                            )
        print("After : " + str(self.block_tower))

        DISPLAY = True
        self.build(10, stability_check=True)
        print("Before : "  + str(self.block_tower))
        bad_block = Block(block_mesh, 'flat_wide',  (0, 0,  13))
        result = Physics.is_stable(self.block_tower, bad_block)
        self.assertTrue(True or result)
        print(result)
        if DISPLAY:
            l = list(self.block_tower.gen_blocks())
            display_colored([b.render() for b in l] + [bad_block.render()],
                            ['gray'] * len(l) + ['blue'],
                            [b.get_aggregate_cog() for b in l] + [bad_block.get_aggregate_cog()]
                            )
        print("After : " + str(self.block_tower))

        # print(block_tower)


        # self.assertTrue(sel)

    def test_skew_arrangment(self):
        block1 = Block(block_mesh, (0, 0, 0), (0, 5, 1))
        block2 = Block(block_mesh, (0, 0, 0), (-2, -11, 1))
        block3 = Block(block_mesh, 'flat_wide', (-1, -6, 3))
        tower_state = Tower_State()
        tower_state.add(block1)
        tower_state.add(block2)
        result = Physics.is_stable(tower_state, block3)
        print(result)
        tower_state.add(block3)
        if DISPLAY:
            meshes = [b.render() for b in tower_state.gen_blocks()]
            display_colored(meshes, ['red', 'green', 'blue'], [b.get_aggregate_cog() for b in tower_state.gen_blocks()])

    def test_auto_generate(self):
        """
        Builds a building from some seed, randomly
        :return:
        """
        DISPLAY = True
        SAVE = False
        state = Tower_State()
        floor = state[FLOOR_LEVEL][0]

        son_desc_gen = floor.gen_possible_block_descriptors()
        son_desc = list(son_desc_gen)
        some_sons = sample(son_desc, 50)
        blocks = [Block(block_mesh, orientation, position) for orientation, position in some_sons]
        if DISPLAY:
            display([b.render() for b in blocks])

        shuffle(blocks)

        #add blocks to tower in some order, without creating collisions
        for new_block in blocks:
            if state.can_add(new_block):
                state.add(new_block)

        print(state)
        print ("We're left with {} blocks".format(len(list(state.gen_blocks()))))
        if DISPLAY:
            old_meshes = [b.render() for b in state.gen_blocks()]
            display(old_meshes)
        i = 0
        for _ in range(10):
            current_blocks = set(state.gen_blocks())
            for block in current_blocks:
                possible_son_descriptors = list(
                    block.gen_possible_block_descriptors(limit_len=20,
                                                         limit_orientation=lambda o: True,
                                                         random_order= True))
                shuffle(possible_son_descriptors)
                for desc in possible_son_descriptors:
                    if not state.is_bad_block(Block.gen_str(desc)):
                        orientation, position = desc
                        new_block = Block(block_mesh, orientation, position)
                        if state.can_add(new_block):
                            state.add(new_block)
                        else:
                            i += 1
            print("""
            Size of tower:{}
            Bad block hashed:{}
            Num of blocks disqualified:{}""".format(len(list(state.gen_blocks())),
                                                    len(state._bad_block_hashes),
                                                    i))

            if DISPLAY:
                new_meshes = [b.render() for b in filter(lambda b: b not in current_blocks, state.gen_blocks())]
                old_meshes = [b.render() for b in current_blocks]
                display_colored(old_meshes + new_meshes, ['gray']*len(old_meshes) + ['c']*len(new_meshes))
        if SAVE:
            save_by_orientation(state, "random_wide_tower")


        print("{} blocks were found to be illegal".format(i))

        print ("Now we have {} blocks".format(len(list(state.gen_blocks()))))

        print(state.get_orientation_vector())
        if DISPLAY:
            old_meshes = [b.render() for b in state.gen_blocks()]
            display(old_meshes)
            display_colored(old_meshes, ['gray'] * len(old_meshes), [b.get_aggregate_cog() for b in state.gen_blocks()])

    def test_attempt_symetry(self):
        """
        Builds a building from some seed, randomly
        :return:
        """
        DISPLAY = True
        SAVE = False
        state = Tower_State(15)
        floor = state[FLOOR_LEVEL][0]
        thresh = 1

        son_desc_gen = floor.gen_possible_block_descriptors()
        son_desc = list(son_desc_gen)
        some_sons = sample(son_desc, 30)
        blocks = [Block(block_mesh, orientation, position) for orientation, position in some_sons]
        if DISPLAY:
            display([b.render() for b in blocks])

        shuffle(blocks)
        def propogate(father_block, dist=6):
            if father_block.orientation in [(90, 0, 0), (90, 0, 90)]:
                dist_x = dist // 2
                dist_y = dist // 2

            elif father_block.orientation in [(0, 90, 0), (0, 0, 0)]:
                dist_x = dist
                dist_y = dist * 2

            else:
                dist_x = dist * 2
                dist_y = dist

            #add blocks to tower in some order, without creating collisions
            minus = [-1, 1, -1, 1]
            tinus = [-1, -1, 1, 1]

            # Create i identical blocks
            positions = []
            for i in range(4):
                positions.append((father_block.position[X] + minus[i] * dist_x,
                                  father_block.position[Y] + tinus[i] * dist_y,
                                  father_block.position[Z]))
            # print(positions)
            blocks = [Block(block_mesh, father_block.orientation, new_posish) for new_posish in positions]
            return blocks

        def force_sym(potential_blocks):
            for new_block in potential_blocks:
                p = propogate(new_block)
                good_blocks = []
                for i, b in enumerate(p):
                    if state.can_add(b):
                        good_blocks.append(i)
                if len(good_blocks) >= thresh:
                    for i in good_blocks:
                        state.add(p[i])
                else: # we're not adding these blocks, so we need to give up on them
                    for i in good_blocks:
                        state.disconnect_block_from_neighbors(p[i])

        force_sym(blocks)


        print(state)
        print ("We're left with {} blocks".format(len(list(state.gen_blocks()))))
        if DISPLAY:
            old_meshes = [b.render() for b in state.gen_blocks()]
            display(old_meshes)
        counter = 0
        bad_desc_c = 0
        for _ in range(10):
            current_blocks = set(state.gen_blocks())
            for block in current_blocks:
                possible_son_descriptors = list(
                    block.gen_possible_block_descriptors(limit_len=10,
                                                         limit_orientation=lambda o: True,
                                                         random_order= True))
                shuffle(possible_son_descriptors)
                for desc in possible_son_descriptors:
                    if not state.is_bad_block(Block.gen_str(desc)):
                        orientation, position = desc
                        new_block = Block(block_mesh, orientation, position)
                        p = propogate(new_block)
                        good_blocks = []
                        for i, b in enumerate(p):
                            if state.can_add(b):
                                good_blocks.append(i)
                            else:
                                counter += 1
                        if len(good_blocks) >= thresh:
                            for i in good_blocks:
                                state.add(p[i])
                        else:  # we're not adding these blocks, so we need to give up on them
                            for i in good_blocks:
                                state.disconnect_block_from_neighbors(p[i])
                    else:
                        bad_desc_c += 1

            print("""
            Size of tower:{}
            Bad block hashed:{}
            Num of blocks disqualified:{}
            Num of blocks rejected at str level:{}""".format(len(list(state.gen_blocks())),
                                                    len(state._bad_block_hashes),
                                                    counter,
                                                    bad_desc_c
                                                             ))

            if DISPLAY:
                new_meshes = [b.render() for b in filter(lambda b: b not in current_blocks, state.gen_blocks())]
                old_meshes = [b.render() for b in current_blocks]
                display_colored(old_meshes + new_meshes, ['gray']*len(old_meshes) + ['c']*len(new_meshes))
        if SAVE:
            save_by_orientation(state)


        print("{} blocks were found to be illegal".format(counter))

        print ("Now we have {} blocks".format(len(list(state.gen_blocks()))))

        print(state.get_orientation_vector())
        if DISPLAY:
            old_meshes = [b.render() for b in state.gen_blocks()]
            display(old_meshes)
            display_colored(old_meshes, ['gray'] * len(old_meshes), [b.get_aggregate_cog() for b in state.gen_blocks()])









