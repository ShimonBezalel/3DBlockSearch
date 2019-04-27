

class Voxel:

    def __init__(self, hub1=None, hub2=None, target=None):
        self.hub1 = hub1
        self.hub2 = hub2
        self.target = target

    def add_hub(self, hub):
        if self.hub1 == None:
            self.hub1 = hub
            if self.target:
                self.target.mark_as_reached()
        elif self.hub2 == None:
            self.hub2 = hub
        else:
            raise AssertionError('Voxel at {} is already full!'.format(self.hub1.position))

    def is_full(self):
        """
        Returns true if no further hubs can be added to this voxel.
        :return:
        """
        return self.hub2 != None

    def get_hubs(self):
        """
        Return a list of the hubs contained within this cell.
        :return:
        """
        return self.hub1, self.hub2
