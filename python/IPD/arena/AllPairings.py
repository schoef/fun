''' Implements line-shaped arena. Agents sit next to each other 
'''

from ArenaBase import ArenaBase
from helpers.memoize import memoize

class AllPairings( ArenaBase ):

    def __init__( self, n = 2 ):
        ''' Initialize arena with agents on a line, playing with their neighbours.
        '''
        self.n = n
        self.positions_ = [ (i,) for i in range(n) ]

        super(AllPairings, self).__init__()

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

    @memoize
    def neighbours( self, position ):
        ''' return all neighbours of a given position on the line.
        '''
        return [p for p in self.positions if p!=position]

    def __str__( self ):
        return ''.join( sorted( str(self.agents[p]) for p in self.positions) )
