import abc
from Agent import Agent
''' Implements Tit for Tat and related strategies
'''

class TFTBase( Agent ):
    ''' Base class for Tit for Tat.
    ''' 


    def __init__( self, behaviour_at_start ):
        self.behaviour_at_start = behaviour_at_start
        return

    def __call__( self, history ):
        ''' TFT repeats the opponents last choice
        '''
        probabilistic = super(TFTBase, self).probabilistic_bahaviour()
        if probabilistic is not None:
            return probabilistic

        if len(history[0])>0:
            return history[1][-1]
        else:
            return self.behaviour_at_start

class TFT( TFTBase ):
    ''' TFT strategy that starts with cooperation
    '''
    def __init__( self ):
        super(TFT, self).__init__( behaviour_at_start = True)

    char = 'T'
    name = 'TFT'
    def __str__( self ):
        return self.char
        
class TFT_SD( TFTBase ):
    ''' TFT strategy that starts with defection 
    '''

    def __init__( self ):
        super(TFT_SD, self).__init__( behaviour_at_start = False)

    char = 't'
    name = 'TFT-D'
    def __str__( self ):
        return self.char

class TFTTBase( Agent ):
    ''' Base class for Tit for two Tats.
    ''' 


    def __init__( self, behaviour_at_start ):
        self.behaviour_at_start = behaviour_at_start
        return

    def __call__( self, history ):
        ''' TFTT recipricates after opponent has repeated twice
        '''
        probabilistic = super(TFTTBase, self).probabilistic_bahaviour()
        if probabilistic is not None:
            return probabilistic

        # if opponent repeated twice, then reciprocate, otherwise do as we did before
        if len(history[0])>1:
            if history[1][-1] == history[1][-2]:
                return history[1][-1]
            else:
                return history[0][-1]
             
        else:
            return self.behaviour_at_start


class TFTT( TFTTBase ):
    ''' TFTT strategy that starts with cooperation
    '''
    def __init__( self ):
        super(TFTT, self).__init__( behaviour_at_start = True)

    char = 'T'
    name = 'TFTT'
    def __str__( self ):
        return self.char
        
class TFTT_SD( TFTTBase ):
    ''' TFTT strategy that starts with defection 
    '''

    def __init__( self ):
        super(TFTT_SD, self).__init__( behaviour_at_start = False)

    char = 't'
    name = 'TFTT-D'
    def __str__( self ):
        return self.char
