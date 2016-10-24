import abc
from Agent import Agent
''' Implements Grudger: Sucker, but only once. 
'''

class Grudger( Agent ):
    ''' Grudger strategy.
    ''' 

    def __call__( self, history, state = {} ):
        ''' Grudger keeps defecting after opponent has defected once. 
        '''
        probabilistic = super(Grudger, self).probabilistic_bahaviour( state )
        if probabilistic is not None:
            return probabilistic

        if state.has_key('grudge') and state['grudge']: return False

        if len(history[0])>0 and history[1][-1] == False:
            state['grudge'] = True
            return False

        return True

    char = 'G'
    name = 'Grudger'
    def __str__( self ):
        return self.char
        
