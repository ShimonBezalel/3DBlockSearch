

class Piece:

    def __init__(self, mesh, orientation, move):
        """

        :param mesh: Object defining shape of piece for rendering
        :param orientation: TODO: Define orientation standard (dice? vector? enum?)
        :param move: spawning parent move
        """
        pass


    def get_hubs(self):
        """
        Returns a list of hubs spawned by this piece
        :return:
        """
        pass

    def copy(self):
        """

        :return:
        """
        #TODO: needed for state copy
        pass

    def get_spawning_move(self):
        pass


    def __str__(self):
        """

        :return:
        """
        pass

    def __eq__(self, other):
        pass

    def __hash__(self):
        pass

