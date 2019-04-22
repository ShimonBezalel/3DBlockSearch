from BlockSearch.block import Block, ORIENTATIONS
from BlockSearch.physics import *
from unittest import TestCase
from stl import mesh
from BlockSearch.display import *
import time

DISPLAY = False #True
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
        self.block_tower = dict()
        self.meshes = []
        results = []
        for b in block_seq[:c]:
            if b.get_top_level() not in self.block_tower:
                self.block_tower[b.get_top_level()] = []
            self.block_tower[b.get_top_level()].append(b)
            self.meshes.append(b.render())
            if stability_check:
                if timeit:
                    start = time.time()
                    Physics.is_stable(self.block_tower, b)
                    elapse = time.time() - start
                    results.append(elapse)
                Physics.is_stable(self.block_tower, b)

        if timeit:
            return results

    def build_tall(self, n):
        """

        :param c: int defining complexity of build
        :return:
        """
        self.block_tower = dict()
        self.meshes = []
        results = []
        for i in range(n):
            b = Block(block_mesh, 'flat_wide', (0, 0, i))
            if b.get_top_level() not in self.block_tower:
                self.block_tower[b.get_top_level()] = []
            self.block_tower[b.get_top_level()].append(b)
            self.meshes.append(b.render())
            start = time.time()
            Physics.is_stable(self.block_tower, b)
            elapse = time.time() - start
            results.append(elapse)


        return results

    def build_kapla(self, n):
        """

        :param c: int defining complexity of build
        :return:
        """
        self.block_tower = dict()
        self.meshes = []
        results = []
        for l in range(0,n,2):
            for i in range(5):
                b = Block(block_mesh, 'flat_wide', (i * 3, 0, l))
                if b.get_top_level() not in self.block_tower:
                    self.block_tower[b.get_top_level()] = []
                self.block_tower[b.get_top_level()].append(b)
                self.meshes.append(b.render())
                start = time.time()
                Physics.is_stable(self.block_tower, b)
                elapse = time.time() - start
                results.append(elapse)
            for i in range(-2, 2):
                b = Block(block_mesh, 'flat_thin', (-7, i * 3, l+1))
                if b.get_top_level() not in self.block_tower:
                    self.block_tower[b.get_top_level()] = []
                self.block_tower[b.get_top_level()].append(b)
                self.meshes.append(b.render())
                start = time.time()
                Physics.is_stable(self.block_tower, b)
                elapse = time.time() - start
                results.append(elapse)


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
        supports = Physics.calculate_below(new_block, self.block_tower[bottom_level - 1])
        if DISPLAY:
            display(self.meshes + [new_block.render()])
            display_colored(self.meshes + [b.render() for b in ([new_block] + supports)],
                            [matte_color] * (len(self.meshes)) + [new_color] + [emphasis_color] * len(supports) )


        self.build(5)
        new_block = Block(block_mesh, 'short_wide', (0, 0, 7))
        bottom_level = new_block.get_bottom_level()
        supports = Physics.calculate_below(new_block, self.block_tower[bottom_level - 1])
        if DISPLAY:
            display(self.meshes + [new_block.render()])
            display_colored(self.meshes + [b.render() for b in ([new_block] + supports)],
                            [matte_color] * (len(self.meshes)) + [new_color] + [emphasis_color] * len(supports))

        self.build(7)
        new_block = Block(block_mesh, 'short_wide', (0, 0, 8))
        bottom_level = new_block.get_bottom_level()
        supports = Physics.calculate_below(new_block, self.block_tower[bottom_level - 1])
        if DISPLAY:
            display(self.meshes + [new_block.render()])
            display_colored(self.meshes + [b.render() for b in ([new_block] + supports)],
                            [matte_color] * (len(self.meshes)) + [new_color] + [emphasis_color] * len(supports))

        new_block = Block(block_mesh, 'tall_thin', (-2, 2, 14))
        bottom_level = new_block.get_bottom_level()
        supports = Physics.calculate_below(new_block, self.block_tower[bottom_level - 1])
        if DISPLAY:
            display(self.meshes + [new_block.render()])
            display_colored(self.meshes + [b.render() for b in ([new_block] + supports)],
                            [matte_color] * (len(self.meshes)) + [new_color] + [emphasis_color] * len(supports))

        self.build(14)
        new_block = Block(block_mesh, 'short_thin', (4, -1, 16))
        bottom_level = new_block.get_bottom_level()
        supports = Physics.calculate_below(new_block, self.block_tower[bottom_level - 1])
        if DISPLAY:
            display(self.meshes + [new_block.render()])
            display_colored(self.meshes + [b.render() for b in ([new_block] + supports)],
                            [matte_color] * (len(self.meshes)) + [new_color] + [emphasis_color] * len(supports))

    def test_stability(self):
        # # test blocks touching the floor
        # self.build(1)
        # first_block = Block(block_mesh, 'short_wide', (-3, 0, 1))
        # stable = Physics.is_stable(self.block_tower, first_block)
        # if DISPLAY:
        #     display(self.meshes + [first_block.render()])
        #
        #
        # self.build(2)
        # new_block = Block(block_mesh, 'short_thin', (-5, 5, 4))
        # Physics.is_stable(self.block_tower, new_block)
        # if DISPLAY:
        #     display(self.meshes + [new_block.render()])


        self.build(14, stability_check=True)
        new_block = Block(block_mesh, 'short_thin', (4, -1, 16))
        Physics.is_stable(self.block_tower, new_block)
        if DISPLAY:
            display(self.meshes + [new_block.render()])

    def test_physics_timing(self):
        #
        # results = self.build(13, stability_check=True, timeit=True)
        # for i, result in enumerate(results):
        #     print ("Time for {} ms: \t {}".format(i + 1, result))

        # results = self.build_tall(300)
        # for i, result in enumerate(results):
        #     print ("Time for {} in s: \t {}".format(i + 1, result))

        results = self.build_kapla(50)
        for i, result in enumerate(results):
            print ("Time for {} in s: \t {}".format(i + 1, result))








