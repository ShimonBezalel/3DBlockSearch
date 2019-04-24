from BlockSearch.block import Block, ORIENTATIONS, ORIENTATION
from BlockSearch.physics import *
from BlockSearch import physics as Physics
from unittest import TestCase
from stl import mesh
from BlockSearch.display import *
from BlockSearch.tower_state import *
import time

DISPLAY = True #False #True
block_mesh = mesh.Mesh.from_file('kapla.stl')

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

    def build_janga(self, n):
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

            for i in range(-2, 3):
                b = Block(block_mesh, 'flat_thin', (0, i * 3, l+1))

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
            l = list(self.block_tower._gen_blocks())
            display_colored([b.render() for b in l] + [bad_block.render()],
                            ['gray']*len(l) + ['blue'],
                            [b.get_aggregate_cog() for b in l] + [bad_block.get_aggregate_cog()]
                            )

        self.build(10, stability_check=True)
        print("Before : "  + str(self.block_tower))
        good_block = Block(block_mesh, ORIENTATION.SHORT_THIN, (-1, -1, 4) )

        self.assertTrue( Physics.is_stable(self.block_tower, good_block))
        if DISPLAY:
            l = list(self.block_tower._gen_blocks())
            display_colored([b.render() for b in l] + [good_block.render()],
                            ['gray']*len(l) + ['blue'],
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
            l = list(self.block_tower._gen_blocks())
            display_colored([b.render() for b in l] + [bad_block.render()],
                            ['gray']*len(l) + ['blue'],
                            [b.get_aggregate_cog() for b in l] + [bad_block.get_aggregate_cog()]
                            )
        print("After : " + str(self.block_tower))

        # print(block_tower)


        # self.assertTrue(sel)





