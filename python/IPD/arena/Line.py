from ArenaBase import ArenaBase
''' Implements line-shaped arena. Agents sit next to each other 
'''

class Line( ArenaBase ):

    def __init__( self, n = 2 ):
        ''' Initialize arena with agents on a line, playing with their neighbours.
        '''
        self.n = n
        self.positions_ = [ (i,) for i in range(n) ]

        super(Line, self).__init__()

        return

    @classmethod
    def fromList( cls, strategies ):
        '''Take strategies and put them on a line, side by side.
        '''
        result = cls(len(strategies))
        result.agents = {p:strategies[ip]() for ip, p in enumerate(result.positions)}
        return result 

    @property
    def positions( self ):
        ''' return all positions 
        '''
        return self.positions_ 

    def neighbours( self, position ):
        ''' return all neighbours of a given position on the line.
        '''
        neighbours = []
        if position[0]>0:          neighbours.append( (position[0]-1,) )
        if position[0]<self.n - 1: neighbours.append( (position[0]+1,) )
        return neighbours 

    def __str__( self ):
        return ''.join( str(self.agents[p]) for p in self.positions) 
