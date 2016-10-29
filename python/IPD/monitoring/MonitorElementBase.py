''' Base class for monitor element 
'''

import abc

class MonitorElementBase:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def initialize_arena( self, arena ):
        return
 
    @abc.abstractmethod
    def add_data( self, arena ):
        ''' Update monitor element with new data 
        '''
        return 

    @abc.abstractmethod
    def write( self ):
        ''' Write monitor element 
        '''
        return 
