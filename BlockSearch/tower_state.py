from BlockSearch.grid import Grid
from BlockSearch.block import Block, Floor
from stl import mesh
from typing import List, Set, Dict, Tuple, Optional, Generator



floor_mesh = mesh.Mesh.from_file('floor.stl')

class Tower_State(Grid):

    def __init__(self, size=30):
        super().__init__()
        self._blocks_by_level: Dict[int: List[Block]] = dict()
        self._blocks_by_level[-1] = [Floor(floor_mesh, size)]
        """
        Remembers bad blocks that should not consume any more time resources
        """
        self._bad_block_hashes = set()

    def add_bad_block(self, block : Block or str):
        """
        Will hash a block, or a string representing a block, and add it to the bad boy list. We assume
        this was not already conducted for this specific block.
        :param block: The block object or it's str representation (not repr! which is cog sensitive)
        :return:
        """
        h = hash(block)
        assert h not in self._bad_block_hashes
        self._bad_block_hashes.add(h)

    def is_bad_block(self, block : Block or str):
        return hash(block) in self._bad_block_hashes

    #todo one of these is wrong
    def get_blocks_by_bottom_level(self):
        return self._blocks_by_level

    def get_blocks_by_top_level(self):
        return self._blocks_by_level

    def _gen_blocks(self, no_floor=True) -> Generator[Block, None, None]:
        # Does not iterate floor
        filter_levels = lambda l: l != -1 if no_floor else lambda l: True
        for level in filter(filter_levels, self._blocks_by_level.keys()):
            for block in self._blocks_by_level[level]:
                yield block


    def add(self, block: Floor or Block):
        if block.get_top_level() not in self._blocks_by_level:
            self._blocks_by_level[block.get_top_level()] = []
        self._blocks_by_level[block.get_top_level()].append(block)

    def render(self, fast=False):
        if not fast:
            meshes = []
            for block in self._gen_blocks():
                meshes.append(block.render())
        else:
            assert False, "not yet implemented"
            meshes = [self._aggregate_mesh()]
        return meshes



    def __str__(self):
        return str(self._blocks_by_level)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __copy__(self):
        pass

    def __getitem__(self, item):
        return self._blocks_by_level.__getitem__(item)

    def keys(self):
        return self._blocks_by_level.keys()





