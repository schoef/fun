''' Monitor fractions of populations
'''

from MonitorElementBase import MonitorElementBase

from strategy.all import *

class PopulationFractions( MonitorElementBase ):

    def __init__ ( self, filename ):
        self.population_data = {}
        self.n = 0  
        self.filename = filename
    
    def initialize_arena( self, arena ):
       self.total_agents = len(arena.positions)

    colors = ['k', 'b', 'g', 'r', 'c', 'm', 'y']
    linestyles  = [ '-', '--', ':', '*', 'x']

    @staticmethod
    def style( i ):
        return PopulationFractions.colors[i%len(PopulationFractions.colors)] + PopulationFractions.linestyles[i/len(PopulationFractions.colors)]

    @property
    def strategies( self ):
        return sorted( self.population_data.keys(), key = lambda s:s.char )

    def add_data( self, arena ):
        ''' Adding population fractions
        '''
        arena_strategies = [ type(arena.agents[p]) for p in  arena.positions ]
        unique_arena_strategies = list(set(arena_strategies))

        # Count known strategies
        for s in self.population_data.keys():
            self.population_data[s].append( arena_strategies.count( s ) )

        # Count strategies not yet known
        for s in unique_arena_strategies:
            if s in self.population_data.keys(): continue
            self.population_data[s] = [0 for i in range(self.n)] + [ arena_strategies.count( s ) ]

        self.n += 1

    def write( self ):
        import numpy as np
        import matplotlib.pyplot as plt

        data_x = xrange(self.n)

        for i_s, s in enumerate( self.strategies ):
            data_y = [ p/float(self.total_agents) for p in self.population_data[s] ]
            #args.extend([data_x, data_y, self.style(i_s)])
            plt.plot( data_x, data_y, self.style(i_s), label=s.name )

        plt.legend(ncol = 3)

        plt.xlim(0, self.n)
        plt.ylim(0, 1)
        plt.xlabel('Generations')
        plt.ylabel('populations')
        plt.grid(True)
        plt.savefig( self.filename )
