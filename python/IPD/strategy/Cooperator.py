import abc
from Agent import Agent

class Cooperator( Agent ):

    def __call__( self, history, state = {} ):

        probabilistic = super(Cooperator, self).probabilistic_bahaviour( state )
        if probabilistic is not None:
            return probabilistic

        return True

    char = 'C'
    name = 'Cooperator'
    def __str__( self ):
        return self.char
