import abc
from Agent import Agent
''' Implements Pavlov: Repeat last choice if outcome was good (CC, DC). 
'''

class Pavlov( Agent ):
    ''' Pavlov strategy.
    ''' 

    def __call__( self, history, state = {} ):
        ''' Pavlov: Repeat last choice if outcome was good (CC, DC). 
        '''
        probabilistic = super(Pavlov, self).probabilistic_bahaviour( state )
        if probabilistic is not None:
            return probabilistic

        if len(history[0])>0:
            if  history[1][-1]:
                return history[0][-1]
            else:
                return not history[0][-1]

        return True

    char = 'P'
    name = 'Pavlov'
    def __str__( self ):
        return self.char
        
