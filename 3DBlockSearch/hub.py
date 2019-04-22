
class Hub:

    TYPE_END_1  = "END_HUB_1"
    TYPE_END_2  = "END_HUB_2"
    TYPE_CENTER = "CENTER_HUB"

    def __init__(self, htype, parent):
        """
        :param htype: One of discreet hub types
        :param orientation: Orientation object of this hub
        :param position:    (X,Y,Z) of the hub
        :param rotation:    (X_deg, Y_deg, Z_deg) rotation of the hub
        :param parent:      Spawning Piece object
        """
        self.htype = htype
        self.parent = parent

    @property
    def orientation(self):
        return self.parent.orientation

    def can_connect(self, other):
        """
        Checks if this hub can sit in a single voxel along with the given other.
        :param other:
        :return:
        """
        if self.htype != other.htype:
            # TODO: Handle END_1 + END_2 cases
            return False

        if self.htype == Hub.TYPE_END_1:
            s = self.orientation
            o = other.orientation

            #      OPTION 1
            # --------+--------
            #   Self  |  Other
            # --------+--------
            #   TOP   |  DOWN
            #   RIGHT |  BACK
            #   FRONT |  RIGHT

            if  (s.top   == o.down) and \
                (s.right == o.back) and \
                (s.front == o.right):
                return True

            #      OPTION 2
            # --------+--------
            #   Self  |  Other
            # --------+--------
            #   TOP   |  ?
            #   RIGHT |  ?
            #   FRONT |  ?


        return False

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
        return self.orientation

    def get_spawning_piece(self):
        """
        returns the parents piece of this hub.
        :return:
        """
        pass

    def __str__(self):
        pass
