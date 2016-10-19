import abc
from ArenaBase import ArenaBase
''' Implements toric arena, i.e. rectangle with periodic boundary conditions 
'''

class Torus( ArenaBase ):

    def __init__( self, nx = 10, ny = 10):
        ''' Initialize toric arena 
        '''
        self.nx = nx
        self.ny = ny
        self.positions_ = [ (i, j) for i in range(nx) for j in range(ny) ]

        super(Torus, self).__init__()

        return 

    @property
    def positions( self ):
        ''' return all positions 
        '''
        return self.positions_ 

    def neighbours( self, position ):
        ''' return all neighbours of a given position
        '''
        neighbours = [ \
            ( (position[0] - 1) % self.nx, (position[1] - 1) % self.ny ), 
            ( (position[0] - 1) % self.nx, (position[1]    ) % self.ny ), 
            ( (position[0] - 1) % self.nx, (position[1] + 1) % self.ny ), 
            ( (position[0]    ) % self.nx, (position[1] - 1) % self.ny ), 
            ( (position[0]    ) % self.nx, (position[1] + 1) % self.ny ), 
            ( (position[0] + 1) % self.nx, (position[1] - 1) % self.ny ), 
            ( (position[0] + 1) % self.nx, (position[1]    ) % self.ny ), 
            ( (position[0] + 1) % self.nx, (position[1] + 1) % self.ny ),
        ] 
        return neighbours 

    def __str__( self ):
        return ''.join( ''.join( str(self.agents[(i, j)]) for i in range( self.nx )) + '\n' for j in range( self.ny) )
