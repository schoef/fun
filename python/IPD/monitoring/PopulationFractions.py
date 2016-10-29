''' Monitor fractions of populations
'''

from MonitorElementBase import MonitorElementBase

from strategy.all import *

class PopulationFractions( MonitorElementBase ):

    def __init__ ( self ):
        self.population_data = {}
        self.n = 0
    
    def initialize_arena( self, arena ):
       self.total_agents = len(arena.positions)

    @property
    def strategies( self ):
        return sorted( self.population_data.keys(), key = lambda s:s.char )

    def add_data( self, arena ):
        ''' Adding population fractions
        '''
        arena_strategies = [ type(arena.agents[p]) for p in  arena.positions ]
        unique_arena_strategies = list(set(arena_strategies))

        # Known strategies
        for s in self.population_data.keys():
            self.population_data[s].append( arena_strategies.count( s ) )

        # New strategies
        for s in unique_arena_strategies:
            if s in self.population_data.keys(): continue
            self.population_data[s] = [0 for i in range(self.n)] + [ arena_strategies.count( s ) ]

        self.n += 1


    def write( self ):
        import numpy as np
        import matplotlib.pyplot as plt

        data_x = xrange(self.n)
        data_y_0 = [ p/float(self.total_agents) for p in self.population_data[self.strategies[0]] ]
        data_y_1 = [ p/float(self.total_agents) for p in self.population_data[self.strategies[1]] ]
        data_y_2 = [ p/float(self.total_agents) for p in self.population_data[self.strategies[2]] ]
        plt.plot(\
                 data_x, data_y_0, 'b-', 
                 data_x, data_y_1, 'g-',
                 data_x, data_y_2, 'r-'
                )
        plt.xlim(0, self.n)
        plt.ylim(0, 1)
        plt.xlabel('Generations')
        plt.ylabel('populations')
        plt.grid(True)

        plt.show()
