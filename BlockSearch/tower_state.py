from copy import copy

from memoized import memoized

from BlockSearch import physics as Physics
from BlockSearch.block import Block, Floor, ORIENTATIONS, RingFloor
from stl import mesh
from typing import List, Set, Dict, Tuple, Optional, Generator
import numpy as np


floor_mesh = mesh.Mesh.from_file('floor.stl')

FLOOR_LEVEL = 0
NEIGHBOR_BELOW = 0
NEIGHBOR_ABOVE = 1
X = 0
Y = 1
Z = 2

class Tower_State():

    _orientation_to_index = dict()
    _index_to_orientation = dict()

    for i, orientation in enumerate(ORIENTATIONS.values()):
        _orientation_to_index[orientation] = i
        _index_to_orientation[i] = orientation


    def __init__(self, size=30, ring_floor=False, father_state=None, *args):
        self._bad_block_calls = 0
        self._order_added = []
        self._updated_top = set()
        self._updated_bottom = set()
        self._updated = set()
        self._mem = set()
        self._max_level = 0
        self._blocks_by_top_level: Dict[int: Set[Block]] = dict()
        self._blocks_by_bottom_level: Dict[int: Set[Block]] = dict()
        self._connectivity: Dict[Block: List[Set[Block], Set[Block]]] = dict()
        if not father_state: # this is son
            if not ring_floor:
                floor = Floor(floor_mesh, size)
            else:
                floor = RingFloor(floor_mesh, size, *args)
            self.floor = floor
            self._blocks_by_top_level[FLOOR_LEVEL] = {floor,}
            self._connectivity[floor] = [set(), set()]
            self._orientation_counter: np.ndarray = np.zeros(shape=(6,))
        else:
            self.floor = None
            self._orientation_counter = None

        #  Remembers bad blocks that should not consume any more time resources
        self._bad_block_hashes = set()
        self._spreads_memory: Dict[Tuple[Block, Block]: Set[Block]] = dict()
        # self._cover_cells_at_level: Dict[int: Set[Tuple[int, int]]] = dict()
        # self._starting_cover_size = (size**2 - (size-3)**2)
        self._father_state: Tower_State = father_state
        self._gen_str()

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

    def stringify_block_neighbors(self, block):
        # A block state can be uniquely described by a block descriptor,
        # along with the number or neighbors above and below.
        # Should a change be made in the future to the neighbors of this block,
        # this will no longer be the same descriptor.
        block_connectivity_symbol = "{}{}{}".format(str(block),
                                                    len(self._connectivity[block][NEIGHBOR_BELOW]),
                                                    len(self._connectivity[block][NEIGHBOR_ABOVE])
                                                    )
        return block_connectivity_symbol

    def add_bad_block_state(self, block : Block):
        stringify = self.stringify_block_neighbors(block)
        self.add_bad_block(stringify)

    def is_bad_block(self, block : Block or str, is_hash=False):
        if not is_hash:
            block = hash(block)
        if not block in self._bad_block_hashes:
            if self._father_state:
                return self._father_state.is_bad_block(block, is_hash=True)
            return False
        self._bad_block_calls += 1
        return True

    def gen_blocks(self, no_floor=True, filter_saturated_block=False) -> Generator[Block, None, None]:
        floor_condition = lambda l: l != FLOOR_LEVEL if no_floor else lambda l: True
        # filter_levels = lambda l: l not in self._updated_top and floor_condition(l)
        filter_levels = lambda l: True and floor_condition(l)
        filter_blocks = lambda b: not b.is_saturated(self) if filter_saturated_block else lambda b: True
        if not no_floor:
            yield self.floor
        if self._father_state:
            for block in self._father_state.gen_blocks(no_floor=no_floor,
                                                       filter_saturated_block=filter_saturated_block):
                yield block
        for block in filter(filter_blocks, self._order_added):
            yield block

        # filter_orientations = orientation_filter if orientation_filter else lambda o: True
        # for level in sorted(filter(floor_condition, self._blocks_by_top_level.keys()), reverse=True):
        #     for block in self._blocks_by_top_level[level]:
        #         yield block
        # if self._father_state:
        #     for block in self._father_state.gen_blocks(no_floor=no_floor, filter_saturated_block=filter_saturated_block):
        #         yield block
        # for level in sorted(filter(filter_levels, self._blocks_by_top_level.keys()), reverse=True):
        #     for block in filter(filter_blocks, self._blocks_by_top_level[level]):
        #         yield block



    # def get_cover_at_level(self, level: int):
    #     """
    #     Cover is all the cells on the XY plane the this building has pieces above. So a cover at a given level is
    #     defined as the projection of the tower onto the XY plane at a given height. Whatever is below the height is
    #     ignored.
    #     :param level:
    #     :return:
    #     """
    #     ret = set()
    #     assert self._father_state is None
    #     for i in filter(lambda l: l in self._cover_cells_at_level, range(level, self._max_level + 1)):
    #         ret |= self._cover_cells_at_level[i]
    #     return ret

    def get_spread(self, block1: Block, block2: Block):
        """
        Retrieves the space between two blocks that can support blocks above, should their center of gravity
        sit within them.
        Spread should only be calculated between blocks that have already been recognized as close enough to hold
        another block above them, otherwise behavior is not defined, or in the best case an assertion will fail.
        This is garanteed by only calling get_spread on blocks both directly under the same piece.
        Spread is commutative
        :param block1:
        :param block2:
        :return:
        """

        assert block1.get_top_level() == block2.get_top_level(), str(block1) + str(block1.get_top_level()) + str(block2) + str(
            block2.get_top_level())

        # a spread with yourself it the cells you cover
        if block1 == block2:
            return block1.get_cover_cells()

        ordered_pair = (block1, block2) if block1 < block2 else (block2, block1)
        if ordered_pair in self._spreads_memory: # shared with father
            return self._spreads_memory[ordered_pair]

        b1_cover_x = {cell[X] for cell in block1.get_cover_cells()}
        b2_cover_x = {cell[X] for cell in block2.get_cover_cells()}

        b1_cover_y = {cell[Y] for cell in block1.get_cover_cells()}
        b2_cover_y = {cell[Y] for cell in block2.get_cover_cells()}

        inter_x = b1_cover_x & b2_cover_x
        inter_y = b1_cover_y & b2_cover_y

        spread = set()
        spread |= block1.get_cover_cells()
        spread |= block2.get_cover_cells()
        if (inter_x):
            union_y = b1_cover_y | b2_cover_y
            min_y = int(min(union_y))
            max_y = int(max(union_y))
            for y in range(min_y, max_y + 1):
                for x in inter_x:
                    spread.add((x, y))

        elif (inter_y):
            union_x = b1_cover_x | b2_cover_x
            min_x = int(min(union_x))
            max_x = int(max(union_x))
            for x in range(min_x, max_x + 1):
                for y in inter_y:
                    spread.add((x, y))

        else:  # no common pieces - skew lines
            """
                                                    X                   XXXXXXX
            XXXXXXX                                 X                               X
                                            or              X       or              X
                    XXXXXXXX                                X                       X


            Relevant for flat pieces only.
            """
            pass
            # See if the candidate blocks above can help increase spread
            candidate_blocks = self.get_blocks_above(block1) & self.get_blocks_above(block2)

            if candidate_blocks:
                flat_block = candidate_blocks.pop()
                center_x, center_y, _ = tuple(flat_block.get_cog())
                skew_center = set()
                for cell in spread:
                    new_cell = ((cell[X] + center_x) // 2, (cell[Y] + center_y) // 2)
                    skew_center.add(new_cell)
                spread |= skew_center

        self._spreads_memory[ordered_pair] = spread
        return spread

    def can_add(self, new_block: Block):
        if not Physics.is_overlapping(self, new_block): # no state changes
            if Physics.is_stable(self, new_block): # no state changes made
                # not_saturated = True
                # for block_below in self.get_blocks_below(new_block):
                #     not_saturated &= not block_below.is_saturated(self, no_changes=True)
                # return True and not_saturated
                return True
        return False

    def add(self, block: Floor or Block):
        """
        Mutatating method for adding a new block to this state. This is by definition a new state!
        :param block: Block, that already underwent all the stages of verification for structural validity
        :return:
        """
        self.confirm(block)
        top = block.get_top_level()
        bottom = block.get_bottom_level()
        if top not in self._blocks_by_top_level:
            self._blocks_by_top_level[top] = set()
        if bottom not in self._blocks_by_bottom_level:
            self._blocks_by_bottom_level[bottom] = set()
        self._blocks_by_top_level[top].add(block)
        self._blocks_by_bottom_level[bottom].add(block)
        self._order_added.append(block)

        # Make additional changes to state for fast grading
        self._orientation_counter[Tower_State._orientation_to_index[block.orientation]] += 1
        self._max_level = max(self._max_level, block.get_top_level())
        self._gen_str()  # update string representation

        # for level in range(bottom, top + 1):
        #     if level not in self._cover_cells_at_level:
        #         self._cover_cells_at_level[level] = set()
        #     self._cover_cells_at_level[level] |= block.get_cover_cells()

    def render(self, fast=False):
        if not fast:
            meshes = []
            for block in self.gen_blocks():
                meshes.append(block.render())
        else:
            assert False, "fast render not yet implemented"
        return meshes

    def get_orientation_vector(self):
        s = np.sum(self._orientation_counter)
        if s != 0:
            return self._orientation_counter / s
        return self._orientation_counter

    def get_top_off(self) -> int:
        """
        Return the heighest level this tower has reached.
        :return:
        """
        return self._max_level

    def get_stability_index(self) -> float:
        """
        Returns a value representing how close this tower is to instability
        :return:
        """
        assert False, "Stability Index not yet implemented"

    def connect_block_to_neighbors(self, catalyst_block: Block):
        """
        Take's given block, searches for it's neighbors, and adds it as their neighbor.
        :param catalyst_block:
        :return:
        """
        # Make changes downwards in the block tower  (recursively)
        #           | | |
        #           V V V
        for neighbor_block in self.get_blocks_below(catalyst_block):
            self.add_block_above(neighbor_block, catalyst_block)
            neighbor_block.reset_aggregate_mesh(self)

        # Make changes upwards in the block tower  (1 level)
        #           ^ ^ ^
        #           | | |
        for neighbor_block in self.get_blocks_above(catalyst_block):
            self.add_block_below(neighbor_block, catalyst_block)

    def disconnect_block_from_neighbors(self, catalyst_block: Block):
        # Reset changes downwards in the block tower  (recursively)
        #           | | |
        #           V V V
        for neighbor_block in self.get_blocks_below(catalyst_block):
            self.remove_block_above(neighbor_block, catalyst_block)
            # resetting the cog's and aggregate meshes is expensive and may be redundant
            neighbor_block.reset_aggregate_mesh(self)

        # Reset changes upwards in the block tower  (1 level)
        #           ^ ^ ^
        #           | | |
        for neighbor_block in self.get_blocks_above(catalyst_block):
            self.remove_block_below(neighbor_block, catalyst_block)

        del self._connectivity[catalyst_block]

    def confirm(self, block):
        # an added block is also a bad block, a block which should never be revisited again.
        self.add_bad_block(block)
        #todo: deprecate this if migrate to block pool

    def set_blocks_below(self, block: Block, blocks: Set[Block] ):
        """
        Permanently links this block to a set of blocks strictly under it, which support it in the air.
        The scheme is assumed to be stable.

        X - Segment of this block
        S - Support blocks
        N - Non support blocks

                        Front View      |            Side View     |          Top View
                        ----------------------------------------------------------------------
                            XXXXXX      |                X         |      NNNNNN
                        N    S   S      |       NNNNNN SSSSSS      |
                                        |                          |                X
                                        |                          |              SSXSSS
                                        |                          |                X
                                        |                          |              SSXSSS

        :param blocks: A list of existing blocks to link as supports
        :return:
        """
        if block not in self._connectivity:
            if self._father_state:
                above = self._father_state.get_blocks_above(block)
            else:
                above = set()
            self._connectivity[block] = [set(), above]
        self._connectivity[block][NEIGHBOR_BELOW] = blocks

    def set_blocks_above(self, block: Block, blocks: Set[Block] ):
        if block not in self._connectivity:
            if self._father_state:
                below = self._father_state.get_blocks_above(block)
            else:
                below = set()
            self._connectivity[block] = [below, set()]
        self._connectivity[block][NEIGHBOR_ABOVE] = blocks

    def get_blocks_below(self, block: Block) -> Set[Block]:
        if block in self._connectivity:
            return self._connectivity[block][NEIGHBOR_BELOW]
        if self._father_state:
            below = self._father_state.get_blocks_below(block)
            above = self._father_state.get_blocks_above(block)
            if below == None:
                # print("Called get blocks below with no block... {}".format(str(block)))
                below = set()
            if above == None:
                # print("Called get blocks below with no block... {}".format(str(block)))
                above = set()
            self._connectivity[block] = [below, above]
            return below

    def get_blocks_above(self, block: Block) -> Set[Block]:
        if block in self._connectivity:
            return self._connectivity[block][NEIGHBOR_ABOVE]
        if self._father_state:
            below = self._father_state.get_blocks_below(block)
            above = self._father_state.get_blocks_above(block)
            if below == None:
                # print("Called get blocks above with no block... {}".format(str(block)))
                below = set()
            if above == None:
                # print("Called get blocks above with no block... {}".format(str(block)))
                above = set()
            self._connectivity[block] = [below, above]
            return above

    def add_block_below(self, block: Block, block_below: Block):
        if block in self._connectivity:
            self._connectivity[block][NEIGHBOR_BELOW].add(block_below)
            return
        if self._father_state:
            below = self._father_state.get_blocks_below(block)
            above = self._father_state.get_blocks_above(block)
            if below == None:
                # print("Called get blocks above with no block... {}".format(str(block)))
                below = set()
            if above == None:
                # print("Called get blocks above with no block... {}".format(str(block)))
                above = set()
            self._connectivity[block] = [below, above]
            self._connectivity[block][NEIGHBOR_BELOW].add(block_below)
            return
        self._connectivity[block] = [{block_below,}, set()]

    def add_block_above(self, block: Block, block_above: Block):
        if block in self._connectivity:
            self._connectivity[block][NEIGHBOR_ABOVE].add(block_above)
            return
        if self._father_state:
            below = self._father_state.get_blocks_below(block)
            above = self._father_state.get_blocks_above(block)
            if below == None:
                # print("Called get blocks above with no block... {}".format(str(block)))
                below = set()
            if above == None:
                # print("Called get blocks above with no block... {}".format(str(block)))
                above = set()
            self._connectivity[block] = [below, above]
            self._connectivity[block][NEIGHBOR_ABOVE].add(block_above)
            return
        self._connectivity[block] = [set(), {block_above,}]

    def remove_block_below(self, block: Block, block_below: Block):
        if block in self._connectivity:
            self._connectivity[block][NEIGHBOR_BELOW].remove(block_below)
            return
        if self._father_state:
            below = self._father_state.get_blocks_below(block)
            above = self._father_state.get_blocks_above(block)
            if below == None:
                # print("Called get blocks above with no block... {}".format(str(block)))
                below = set()
            if above == None:
                # print("Called get blocks above with no block... {}".format(str(block)))
                above = set()
            self._connectivity[block] = [below, above]
            self._connectivity[block][NEIGHBOR_BELOW].remove(block_below)
            return
        self._connectivity[block] = [set(), set()]

    def remove_block_above(self, block: Block, block_above: Block):
        if block in self._connectivity:
            self._connectivity[block][NEIGHBOR_ABOVE].remove(block_above)
            return
        if self._father_state:
            below = self._father_state.get_blocks_below(block)
            above = self._father_state.get_blocks_above(block)
            if below == None:
                # print("Called get blocks above with no block... {}".format(str(block)))
                below = set()
            if above == None:
                # print("Called get blocks above with no block... {}".format(str(block)))
                above = set()
            self._connectivity[block] = [below, above]
            self._connectivity[block][NEIGHBOR_ABOVE].remove(block_above)
            return
        self._connectivity[block] = [set(), set()]

    def _gen_str(self):
        self._str = str(sorted(list(self.gen_blocks())))

    def __str__(self):
        return self._str

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def __copy__(self):
        """
        This function needed to be meticulously designed so that copies would be skeletal, and light at possible.
        Therefore, no deep-copies are used. Characteristics that are unique to a tower state and all its sons are
        kept through use of recursion.
        :return:
        """
        # It is important to emphasize that a copied state is only a replica as a son of this father state.
        copied_state = Tower_State(self.floor.get_size(), father_state=self)
        copied_state.floor                   = self.floor
        copied_state._max_level              = self._max_level
        copied_state._orientation_counter    = copy(self._orientation_counter)
        copied_state._spreads_memory         = self._spreads_memory # invarient of state
        copied_state._bad_block_calls        = self._bad_block_calls

        return copied_state

    def get_by_top(self, level):
        s = set()
        if level in self._blocks_by_top_level:
            s |= self._blocks_by_top_level[level]
        if self._father_state and level not in self._updated_top:
            s |= self._father_state.get_by_top(level)
            self._blocks_by_top_level[level] = s
            self._updated_top.add(level)
        return s

    def get_by_bottom(self, level):
        s = set()
        if level in self._blocks_by_bottom_level:
            s |= self._blocks_by_bottom_level[level]
        if self._father_state and level not in self._updated_bottom:
            s |= self._father_state.get_by_bottom(level)
            self._blocks_by_bottom_level[level] = s
            self._updated_bottom.add(level)
        return s

    def __contains__(self, item):
        if item in self._mem:
            return True

        if item in self._blocks_by_bottom_level or item in self._blocks_by_top_level:
            self._mem.add(item)
            return True

        if self._father_state and item in self._father_state:
            return True
        return False


    def keys(self):
        if self._father_state:
            return self._blocks_by_top_level.keys() | self._father_state.keys()
        return self._blocks_by_top_level.keys()





