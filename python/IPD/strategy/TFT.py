import abc
from Agent import Agent
''' Implements Tit for Tat
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


class TFT_start_cooperate( TFTBase ):
    ''' TFT strategy that starts with cooperation
    '''
    def __init__( self ):
        super(TFT_start_cooperate, self).__init__( behaviour_at_start = True)

    char = 'T'
    name = 'TFT'
    def __str__( self ):
        return self.char
        
class TFT_start_defect( TFTBase ):
    ''' TFT strategy that starts with defection 
    '''

    def __init__( self ):
        super(TFT_start_defect, self).__init__( behaviour_at_start = False)

    char = 't'
    name = 'TFT-D'
    def __str__( self ):
        return self.char
