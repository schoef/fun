import abc
from Agent import Agent

from helpers.PrisonerDilemma import PrisonerDilemma

''' Implements Adaptive: Starts with c,c,c,c,c,c,d,d,d,d,d and then takes choices which have given the best average score re-calculated after every move.  
'''

class Adaptive( Agent ):
    ''' Adaptive strategy.
    ''' 


    def __call__( self, history, state = {} ):
        ''' Adaptive: Starts with c,c,c,c,c,c,d,d,d,d,d and then takes choices which have given the best average score re-calculated after every move. 
        '''
        
        if not state.has_key('sequence'): 
            state['sequence'] = [True, True, True, True, True, True, False, False, False, False, False]

        # Update performance measurements with previous game 
        if len(history[0])>1:
            if not state.has_key('count'): state['count'] = {}
            if not state.has_key('revenue'): state['revenue'] = {}

            opponent = history[1][-2]
            reaction = history[0][-1]
            revenue  = PrisonerDilemma.revenue( history[0][-1], history[1][-1] )[0]
            s_key = (opponent, reaction)
            for key, val in [['count', 1], ['revenue', revenue]]: 
                if state[key].has_key( s_key ): 
                    state[key][s_key] += val
                else:
                    state[key][s_key]  = val

        # Play start sequence
        if len( state['sequence'] ) > 0:
            result = state['sequence'][0]
            del state['sequence'][0]
            return result

        # Probabilistic
        probabilistic = super(Adaptive, self).probabilistic_bahaviour( state )
        if probabilistic is not None:
            return probabilistic

        # Make adaptive choice
        opponent = history[1][-1]
        if state['revenue'].has_key((opponent, False)) and state['revenue'].has_key((opponent, True)):
            defect_expectation      = state['revenue'][(opponent, False)]/float(state['count'][(opponent, False)]) if state['count'][(opponent, False)] > 0 else 0
            cooperation_expectation = state['revenue'][(opponent, True)] /float(state['count'][(opponent, True)])  if state['count'][(opponent, True)] > 0 else 0

            # print opponent, 'D', defect_expectation,'C', cooperation_expectation
            return cooperation_expectation >= defect_expectation
        else:
            return True

    char = 'A'
    name = 'Adaptive'
    def __str__( self ):
        return self.char
        
