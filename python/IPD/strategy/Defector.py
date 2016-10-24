import abc
from Agent import Agent

class Defector( Agent ):

    def __call__( self, history, state = {} ):

        probabilistic = super(Defector, self).probabilistic_bahaviour( state )
        if probabilistic is not None:
            return probabilistic

        return False

    char = 'D'
    name = 'Defector'
    def __str__( self ):
        return self.char
