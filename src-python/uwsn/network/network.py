import config as cf

from .node import Node

from ..utils.utils import *
from ..utils.tracer import Tracer

import matplotlib.pyplot as plt

class Network(list):
    def __init__(self, init_nodes=None):
        print('Instantiating nodes...')
        if init_nodes:
            self.extend(init_nodes)
        else:
            nodes = [Node(i, self) for i in range(0, cf.NB_NODES)]
            self.extend(nodes)
            # last node in nodes is the base station
            base_station = Node(cf.BSID, self)
            base_station.pos_x = cf.BS_POS_X
            base_station.pos_y = cf.BS_POS_Y
            self.append(base_station)
        
        self._dict = {}
        for node in self:
            self._dict[node.id] = node

        print("Nodes instantiated.")

        self.perform_two_level_comm = 1
        self.round = 0
        self.centroids = []
        self.routing_protocol = None
        self.sleep_scheduler_class = None

        self.initial_energy = self.get_remaining_energy()
        self.first_depletion = 0
        self.per30_depletion = 0
        self.energy_spent = []

    def get_remaining_energy(self, ignore_nodes=None):
        """Returns the sum of the remaining energies at all nodes."""
        set_nodes = self.get_alive_nodes()
        if len(set_nodes) == 0:
            return 0
        if ignore_nodes:
            set_nodes = [node for node in set_nodes if node not in ignore_nodes]
        transform = lambda x: x.energy_source.energy
        energies = [transform(x) for x in set_nodes]
        return sum(x for x in energies)
    
    
    def get_alive_nodes(self):
        """Return nodes that have positive remaining energy."""
        return [node for node in self[0:-1] if node.alive]