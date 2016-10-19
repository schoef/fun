''' Base class of an Agent playing the iterated prisoners dilemma
'''

import abc
import random

class Agent:
    __metaclass__ = abc.ABCMeta

    def __init__( self ):
        self.probability_of_random_response = 0

    def probabilistic_bahaviour( self ):
        ''' If one of the properties is defined, act accordingly
        '''
        # give a random answer in 'probability_random' of the cases
        if hasattr(self, "probability_random"):
            if random.uniform(0,1)<self.probability_random:
                return bool(random.getrandbits(1)) 
        if hasattr(self, "probability_defect"):
            if random.uniform(0,1)<self.probability_defect:
                return False
        if hasattr(self, "probability_cooperate"):
            if random.uniform(0,1)<self.probability_cooperate:
                return True
    
    @abc.abstractmethod
    def __call__( self, history ):
        ''' Implement the strategy based on the history
        '''
        return 

    @abc.abstractmethod
    def __str__( self ):
        ''' How to print yourself 
        '''
        return 

# The following functions create new classes that have modified behaviour
def probability_random(cls,  val, char = None, name = None):
    ''' Give a random behaviour in 'val' fraction of cases
    '''
    args = {'probability_random':val}
    if char is not None: args['char'] = char
    if name is not None: args['name'] = name
    return type(cls.__name__+'_probrand_%i'%(100*val), (cls,), args)
def probability_defect(cls,  val, char = None, name = None):
    ''' Defect in 'val' fraction of cases
    '''
    args = {'probability_defect':val}
    if char is not None: args['char'] = char
    if name is not None: args['name'] = name
    return type(cls.__name__+'_probdef_%i'%(100*val), (cls,), args)
def probability_cooperate(cls,  val, char = None, name = None):
    ''' Cooperate in 'val' fraction of cases
    '''
    args = {'probability_cooperate':val}
    if char is not None: args['char'] = char
    if name is not None: args['name'] = name
    return type(cls.__name__+'_probcoop_%i'%(100*val), (cls,), args)
