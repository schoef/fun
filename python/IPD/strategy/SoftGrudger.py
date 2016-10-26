import abc
from Agent import Agent

''' SoftGrudger - Co-operates until the opponent defects, in such case opponent is punished with d,d,d,d,c,c.   
'''

class SoftGrudger( Agent ):
    ''' SoftGrudger strategy.
    ''' 

    def __call__( self, history, state = {} ):
        ''' SoftGrudger:  Co-operates until the opponent defects, in such case opponent is punished with d,d,d,d,c,c.  
        '''

        if not state.has_key('sequence'): 
            state['sequence'] = []
        
        # Start with cooperation
        if len(history[0])==0: 
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
                probabilistic = super(SoftGrudger, self).probabilistic_bahaviour( state )
                if probabilistic is not None:
                    return probabilistic
                return True
            # otherwise retaliate with DDDDCC 
            else:
                state['sequence'] = [False for i in range(3)] + [True, True]
                return False 

    char = 'S'
    name = 'SoftGrudger'
    def __str__( self ):
        return self.char
        
