import abc
from ArenaBase import ArenaBase
''' Implements toric arena, i.e. rectangle with periodic boundary conditions 
'''

class Rectangle( ArenaBase ):

    def __init__( self, nx = 10, ny = 10):
        ''' Initialize toric arena 
        '''
        self.nx = nx
        self.ny = ny
        self.positions_ = [ (i, j) for i in range(nx) for j in range(ny) ]

        super(Rectangle, self).__init__()

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
            ( position[0] - 1, position[1] - 1), 
            ( position[0] - 1, position[1]    ), 
            ( position[0] - 1, position[1] + 1), 
            ( position[0]    , position[1] - 1), 
            ( position[0]    , position[1] + 1), 
            ( position[0] + 1, position[1] - 1), 
            ( position[0] + 1, position[1]    ), 
            ( position[0] + 1, position[1] + 1),
        ] 
        return filter( lambda p:p[0]>=0 and p[1]>=0 and p[0]<self.nx and p[1]<self.ny, neighbours )

        
    def __str__( self ):
        return ''.join( ''.join( str(self.agents[(i, j)]) for i in range( self.nx )) + '\n' for j in range( self.ny) )
