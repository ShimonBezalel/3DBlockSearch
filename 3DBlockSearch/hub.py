
class Hub:

    TYPE_END    = "END_HUB"
    TYPE_CENTER = "CENTER_HUB"

    def __init__(self, type, position, rotation, parent):
        """
        :param type: One of discreet hub types
        :param orientation: TODO: Define orientation standard (dice? vector? enum?)
        :param position:    (X,Y,Z) of the hub
        :param rotation:    (X_deg, Y_deg, Z_deg) rotation of the hub
        :param parent:      Spawning Piece object
        """
        self.type = type
        self.position = position
        self.rotation = rotation
        self.parent = parent

    def can_connect(self, other):
        """
        Checks if this hub can sit in a single voxel along with the given other.
        :param other:
        :return:
        """
        if self.type == Hub.TYPE_END:


    def get_connectible_pieces(self):
        """
        Returns a list of potential pieces that can connect to this hub.
        The pieces are defined by thier positions and orientation relative to this hub.
        :return:
        """
        pass

    def get_type(self):
        pass

    def get_orientation(self):
        pass

    def get_spawning_piece(self):
        """
        returns the parents piece of this hub.
        :return:
        """
        pass

    def __str__(self):
        pass
