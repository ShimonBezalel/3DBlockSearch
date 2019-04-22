from BlockSearch.block import Block, ORIENTATIONS, ORIENTATION
from unittest import TestCase
from stl import mesh
from BlockSearch.display import display, display_cells, display_multiple_cells, display_multiple_grids

DISPLAY = False #True
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
        overlapping_blocks.append(Block(block_mesh, (90, 90, 0), (0, 0, 1)))    # 1
        overlapping_blocks.append(Block(block_mesh, (90, 0, 0), (0, 7, 0)))     # 2
        overlapping_blocks.append(Block(block_mesh, (90, 0, 0), (0, -7, 0)))    # 3
        overlapping_blocks.append(Block(block_mesh, (90, 0, 0), (0, 0, 0)))     # 4
        for i, block in enumerate(overlapping_blocks):
            if DISPLAY:
                display([b.render() for b in [block1, block]])
                display_multiple_cells([b.get_cells() for b in [block1, block]], scale=10)
            self.assertTrue(block1.is_overlapping(block),
                            "Block {} found not to be overlapping! Joint cells:{}".format(i, str(block.get_cells() & block1.get_cells())))

        if DISPLAY:
            display([b.render() for b in [block1] + overlapping_blocks])

        #Non- Overlapping
        not_overlapping_blocks = []
        not_overlapping_blocks.append(Block(block_mesh, (0, 0, 0), (30, 0, 0)))     # 0
        not_overlapping_blocks.append(Block(block_mesh, (0, 0, 0), (0, 0, 10)))     # 1
        not_overlapping_blocks.append(Block(block_mesh, (0, 0, 0), (0, 0, 5)))      # 2
        not_overlapping_blocks.append(Block(block_mesh, (90, 90, 0),(0, 0, 2)))     # 3


        for i, block in enumerate(not_overlapping_blocks):
            if DISPLAY:
                display([b.render() for b in [block1, block]])
                display_multiple_cells([b.get_cells() for b in [block1, block]], scale=10)
            self.assertTrue(not block1.is_overlapping(block),
                            "Block {} found to be overlapping!\n Joint cells:{}".format(i, str(block.get_cells() & block1.get_cells())))

        if DISPLAY:
            display([b.render() for b in [block1] + not_overlapping_blocks])

    def test_orientation(self):
        block1 = Block(block_mesh, (0,  0, 0), (0, 0, 0))
        block2 = Block(block_mesh, 'short_wide', (0, 0, 0))
        block3 = Block(block_mesh, ORIENTATION.SHORT_WIDE, (0, 0, 0))
        self.assertEqual(block1.get_cells(), block2.get_cells())
        self.assertEqual(block1.get_cells(), block3.get_cells())

    def test_cells(self):
        blocks = []
        for i, orientation in enumerate(ORIENTATIONS):
            blocks.append(Block(block_mesh, orientation, ((-1)**i * i *10, (-1)**(i + 1) * i * 10, 0)))


        if DISPLAY:
            display_multiple_cells([block.get_cells() for block in blocks])

    def test_cover_cells(self):
        blocks = []
        for i, orientation in enumerate(ORIENTATIONS):
            blocks.append(Block(block_mesh, orientation, ((-1)**i * i *5, (-1)**(i + 1) * i * 5, 0)))


        if DISPLAY:
            display_multiple_grids([block.get_cover_cells() for block in blocks])

    def test_spread(self):
        #same orientation
        orientation = 'tall_wide'
        block1 = Block(block_mesh, orientation, (0, 0, 0))
        block2 = Block(block_mesh, orientation, (2, 1, 0))

        spread = block1.get_spread(block2)
        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread], scale=20)

        orientation = 'short_wide'
        block1 = Block(block_mesh, orientation, (0, 0, 0))
        block2 = Block(block_mesh, orientation, (5, 5, 0))

        spread = block1.get_spread(block2)
        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread], scale=20)

        orientation = 'flat_thin'
        block1 = Block(block_mesh, orientation, ( 0,  0, 0))
        block2 = Block(block_mesh, orientation, (10, 10, 0))

        spread = block1.get_spread(block2)
        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread], scale=20)

        # differing orientations - must have same top level
        block1 = Block(block_mesh, 'flat_wide', ( 0,  0, 0))
        block2 = Block(block_mesh, 'tall_thin', ( 5, 3, -7))

        spread = block1.get_spread(block2)
        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread], scale=20)

        block1 = Block(block_mesh, 'flat_wide', ( 0,  0, 1))
        block2 = Block(block_mesh, 'short_thin', ( -10, 3, 0))

        spread = block1.get_spread(block2)
        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread], scale=20)


        # test commutative quality of spread: ie. my spread with you is the same as yours spread with me.
        block1 = Block(block_mesh, 'flat_wide', ( 0,  0, 1))
        block2 = Block(block_mesh, 'short_thin', ( -15, 5, 0))

        spread1 = block1.get_spread(block2)
        spread2 = block1.get_spread(block2)

        self.assertEqual(spread1, spread2)

        if DISPLAY:
            display([block1.render(), block2.render()])
            display_multiple_cells([block1.get_cells(), block2.get_cells()], scale=20)
            display_multiple_grids([block1.get_cover_cells(), block2.get_cover_cells(), spread1, spread2], scale=20)


        # cases for empty spreads - should never happen!
        block1 = Block(block_mesh, (0, 0, 0), ( 0,  0, 0))
        block2 = Block(block_mesh, (0, 0, 0), ( -15, -15, 0))
        with self.assertRaises(AssertionError):
            spread1 = block1.get_spread(block2)

        if DISPLAY:
            display([block1.render(), block2.render()])


    def test_mesh(self):
        block1 = Block(block_mesh, (0, 0, 0), ( 0,  0, 0))
        print(block1)
        if DISPLAY:
            display([block1.render()])

    def test_levels(self):
        #same orientation
        orientation = 'tall_wide'
        block1 = Block(block_mesh, orientation, (0, 0, 0))
        block2 = Block(block_mesh, orientation, (2, 1, 0))

        print(block1.get_top_level())
        print(block2.get_top_level())
        self.assertTrue(block1.get_top_level() == block2.get_top_level())

        print(block1.get_bottom_level())
        print(block2.get_bottom_level())
        self.assertTrue(block1.get_bottom_level() == block2.get_bottom_level())

        # differing orientations
        block1 = Block(block_mesh, 'flat_wide', ( 0,  0, 0))
        block2 = Block(block_mesh, 'tall_thin', ( 5, 3, -7))

        print(block1.get_top_level())
        print(block2.get_top_level())
        self.assertTrue(block1.get_top_level() == block2.get_top_level())

        print(block1.get_bottom_level())
        print(block2.get_bottom_level())
        self.assertTrue(block1.get_bottom_level() > block2.get_bottom_level())



