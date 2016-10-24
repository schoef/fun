import abc
from Agent import Agent
import random

class Random( Agent ):

    def __call__( self, history, state = {} ):

        probabilistic = super(Random, self).probabilistic_bahaviour( state )
        if probabilistic is not None:
            return probabilistic

        return bool(random.getrandbits(1)) 

    char = 'R'
    name = 'Random'
    def __str__( self ):
        return self.char
