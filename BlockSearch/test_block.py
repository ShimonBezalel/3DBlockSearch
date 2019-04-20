from BlockSearch.block import Block, ORIENTATIONS
from unittest import TestCase
from stl import mesh
from BlockSearch.display import display

DISPLAY = True #False #True
block_mesh = mesh.Mesh.from_file('kapla.stl')

class Block_Test(TestCase):


    def test_constructor(self):
        block1 = Block(block_mesh, (0, 0, 0), (0, 0, 0))
        self.assertEqual(list(block1.get_cog()), [0, 0, 0])
        if DISPLAY:
            print(str(block1))
            display([block1.render()])

    def test_translate(self):
        block1 = Block(block_mesh, (0, 0, 0), (10, 10, 10))
        self.assertEqual(list(block1.get_cog()), [10, 10, 10])
        if DISPLAY:
            print(str(block1))
            display([block1.render()])

    def test_rotate(self):
        blocks = []
        for orientation in ORIENTATIONS:
            blocks.append(Block(block_mesh, orientation, (0, 0, 0)))
        for block in blocks:
            self.assertEqual(list(block.get_cog()), [0, 0, 0])
        if DISPLAY:
            for b in blocks:
                print (b)
            display([b.render() for b in blocks])

        with self.assertRaises(AssertionError):
            Block(block_mesh, (-90, -90, -90), (0, 0, 0))

    def test_overlap(self):
        block1 = Block(block_mesh, (0, 0, 0), (0, 0, 0))

        #Overlapping
        overlapping_blocks = []

        overlapping_blocks.append(Block(block_mesh, (0, 0, 0), (0, 0, 0)))      # 0
        overlapping_blocks.append(Block(block_mesh, (90, 90, 0), (0, 0, 2.5)))  # 1
        overlapping_blocks.append(Block(block_mesh, (90, 0, 0), (0, 7, 0)))     # 2
        overlapping_blocks.append(Block(block_mesh, (90, 0, 0), (0, -7, 0)))    # 3
        overlapping_blocks.append(Block(block_mesh, (90, 0, 0), (0, 0, 0)))     # 4
        for i, block in enumerate(overlapping_blocks):
            if DISPLAY:
                display([b.render() for b in [block1, block]])
            self.assertTrue(block1.is_overlapping(block),
                            "Block {} found not to be overlapping! Joint cells:{}".format(i, str(block.get_cells() & block1.get_cells())))

        if DISPLAY:
            display([b.render() for b in [block1] + overlapping_blocks])

        #Non- Overlapping
        not_overlapping_blocks = []
        not_overlapping_blocks.append(Block(block_mesh, (0, 0, 0), (30, 0, 0)))     # 0
        not_overlapping_blocks.append(Block(block_mesh, (0, 0, 0), (0, 0, 10)))     # 1
        not_overlapping_blocks.append(Block(block_mesh, (0, 0, 0), (0, 0, 5)))      # 2
        for i, block in enumerate(not_overlapping_blocks):
            if DISPLAY:
                display([b.render() for b in [block1, block]])
            self.assertTrue(block1.is_overlapping(block),
                            "Block {} found to be overlapping!\n Joint cells:{}".format(i, str(block.get_cells() & block1.get_cells())))

        if DISPLAY:
            display([b.render() for b in [block1] + not_overlapping_blocks])