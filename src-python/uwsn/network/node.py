import config as cf
import numpy as np

from .energy import EnergySource, Battery, PluggedIn

class Node(object):
    def __init__(self,id,parent=None):
        self.position = np.random.randint(-50,50,size =(1,3)).tolist()[0]
        # print(self.position)
        self.x = self.position[0]
        self.y = self.position[1]
        self.z = self.position[2]

        if id == cf.BSID:
            self.energy_source = PluggedIn(self)
        else:
            self.energy_source = Battery(self)

        self.id = id
        self.network = parent

        self.reactivate()

    def reactivate(self):
        """Reactivate nodes for next simulation."""
        self.alive = 1
        self.tx_queue_size = 0
        self._next_hop = cf.BSID
        self.distance_to_endpoint = 0
        self.amount_sensed = 0
        self.amount_transmitted = 0
        self.amount_received = 0
        self.membership = cf.BSID
        # aggregation function determines the cost of forwarding messages
        # (in number of bits)
        self.aggregation_function = lambda x: 0
        self.time_of_death = cf.INFINITY
        self._is_sleeping = 0
        self.sleep_prob = 0.0
        # for coverage purposes
        self.neighbors = []
        self.nb_neighbors = -1
        self.exclusive_radius = 0        
