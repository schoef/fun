import abc
from Agent import Agent

''' Gradual - Co-operates until the opponent defects, in such case defects the total number of times the opponent has defected during the game. Followed up by two co-operations.  
'''

class Gradual( Agent ):
    ''' Gradual strategy.
    ''' 

    def __call__( self, history, state = {} ):
        ''' Gradual:  Co-operates until the opponent defects, in such case defects the total number of times the opponent has defected during the game. Followed up by two co-operations. 
        '''

        if not state.has_key('sequence'): 
            state['sequence'] = []
        
        # Count defections 
        if not state.has_key('count_defections'): state['count_defections'] = 0
        if len(history[0])>0:
            if history[1][-1] == False: state['count_defections'] += 1
        # Start with cooperation
        else:
            return True

        # Play sequence
        if len( state['sequence'] ) > 0:
            result = state['sequence'][0]
            del state['sequence'][0]
            return result
        else:
            # If opponent cooperated, cooperate
            if history[1][-1] == True: 
                # Probabilistic
                probabilistic = super(Gradual, self).probabilistic_bahaviour( state )
                if probabilistic is not None:
                    return probabilistic
                return True
            # otherwise retaliate total number of times opponent has defected followed by two cooperations. 
            else:
                state['sequence'] = [False for i in range(state['count_defections'] - 1)] + [True, True]
                return False 
                


    char = 'G'
    name = 'Gradual'
    def __str__( self ):
        return self.char
        
