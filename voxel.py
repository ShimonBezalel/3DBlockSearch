
class Voxel:


    def __init__(self, type, orientation, parent):
        """

        :param type: One of discreet voxel types
        :param orientation: TODO: Define orientation standard (dice? vector? enum?)
        :param parent: spawning piece
        """
        pass

    def can_connect(self, other):
        """
        Checks if this voxel can sit in a single cell along with the given other.
        :param other:
        :return:
        """
        pass

    def get_connectible_pieces(self):
        """
        Returns a list of potential pieces that can connect to this voxel.
        The pieces are defined by thier positions and orientation relative to this voxel.
        :return:
        """
        pass

    def get_type(self):
        pass

    def get_orientation(self):
        pass

    def get_spawning_piece(self):
        """
        returns the parents piece of this voxel.
        :return:
        """
        pass

    def __str__(self):
        pass
