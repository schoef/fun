''' Base class for an arena where Agents play IPD 
'''

#Helpers
from helpers.PrisonersDilemma import PrisonersDilemma
from helpers.memoize import memoize

import abc
import random

class ArenaBase:
    __metaclass__ = abc.ABCMeta
    
    def __init__( self ):
        ''' Initialize the ArenaBase 
        '''
  
        # Define all pairs of positions that play with each other 
        self.pairs   = list( set ( [ tuple(sorted( (p, q) )) for p in self.positions for q in self.neighbours( p ) ] ))

        # 'history' (list of past decisions of the two agents in each pair) and 'state' (dictionary defining the state
        # of the agent playing against the opponent in the pair) completely define the decision of the agent.
        # In particular, agent classes can not have an internal states as there is one agent per position playing against several opponents.
        # Initialize empty history and state

        self.history = { pair:[[],[]] for pair in self.pairs }
        self.state   = { pair:{p:{} for p in pair} for pair in self.pairs }

        self.max_history_length = 3

        self.__monitoring_elements = []
         
        return 

    @abc.abstractproperty
    def positions( self ):
        ''' return all positions 
        '''
        return 

    @abc.abstractmethod
    def neighbours( self, position ):
        ''' return all neighbours of a given position
        '''
        return 

    @abc.abstractmethod
    def __str__( self ):
        return 

    def initialize( self, strategy ):
        ''' Initialze positions uniformly with agents.
        '''
        self.agents = {p:strategy() for p in self.positions}

    def initialize_random( self, strategies ):
        ''' Initialze positions randomly with Agents.
        '''
        self.agents = {p:strategies[random.randint(0, len(strategies)-1 )]() for p in self.positions}

    @memoize
    def agent_neighbour_count( self, p ):
        return len( self.neighbours( p ) )

    def run_agents( self ):
        ''' Let all player pairs play, increment the agents revenues and add result to history
        '''
        # Revenue per Agent
        self.agent_revenue = {p:0. for p in self.positions}
        # Revenue per pair
        self.pair_revenues = {p:(None, None) for p in self.pairs}
        for pair in self.pairs:
            a1, a2 = pair

            # Play!
            decision_agent1 = self.agents[a1]( history = self.history[pair],                    state = self.state[pair][a1] )
            decision_agent2 = self.agents[a2]( history = list(reversed(self.history[pair])),    state = self.state[pair][a2] )

            revenue_agent1, revenue_agent2 = PrisonersDilemma.revenue( decision_agent1, decision_agent2 )

            self.pair_revenues[pair] = (revenue_agent1, revenue_agent2) 

            # Increment revenue and count of games
            self.agent_revenue[a1] += revenue_agent1
            self.agent_revenue[a2] += revenue_agent2

            # Add game to mutual history
            self.history[pair][0].append( decision_agent1 )
            self.history[pair][1].append( decision_agent2 )

            if self.max_history_length is not None:
                self.history[pair][0] = self.history[pair][0][-self.max_history_length:] 
                self.history[pair][1] = self.history[pair][1][-self.max_history_length:] 
                
    def evaluate_performance( self ):
        ''' Calculate perforamce figures based on agent revenues (Normalized by number of neighbours)
        '''
        # Evaluate the performance of each agent by averaging
        self.agent_average_performance = {p:self.agent_revenue[p]/self.agent_neighbour_count(p) for p in self.positions}

        # Accumulating results per strategy
        self.population_performance_cumulative    = {}
        self.population_count          = {}
        for p in self.positions:
            strategy = type(self.agents[p])
            if strategy not in self.population_performance_cumulative.keys():
                self.population_performance_cumulative[strategy]  = self.agent_average_performance[p]
                self.population_count[strategy]        = 1
            else:
                self.population_performance_cumulative[strategy]  += self.agent_average_performance[p]
                self.population_count[strategy]        += 1
            
        # Averaging strategy performance
        self.population_performance = {}
        for strategy in self.population_performance_cumulative.keys():
            self.population_performance[strategy] = self.population_performance_cumulative[strategy]/self.population_count[strategy]

    def evolve_arena( self ):
        '''Evolve agents based on the agents performance.
        An agent is removed if all neighbours perform better. 
        It is replaced by a random choice among the neighbours with the best performance.
        Histories of the affected pairs are reset.
        '''
        
        replacements = []
        for p in self.positions:
            neighbour_performances = {q:self.agent_average_performance[q] for q in self.neighbours( p )}
            # find local performance minima
            if all( self.agent_average_performance[p] <= performance for performance in neighbour_performances.values()):
                # find best performing neighbour strategies
                maximum_performance = max(neighbour_performances.values())
                winners = [type(self.agents[q]) for q in neighbour_performances.keys() if self.agent_average_performance[q]==maximum_performance] 
                # select random winner if multiple strategies
                #print agent_average_performance[p], maximum_performance, neighbour_performances.values(), winners
                if len(winners)>1:
                    winner = winners[ random.randrange(0, len(winners)) ] 
                else:
                    winner = winners[0]
                replacements.append( (p, winner) )

        # Replace looser with winner instance, delete history with neighbours and reset states
        for pos, winner in replacements:
            if type(self.agents[pos]) == winner:
                continue

            #print "Replacing %r with %r" % ( type(self.agents[pos]), winner) 

            self.agents[pos] = winner()
            for q in self.neighbours( p ):
                pair = tuple(sorted(( p, q )))
                self.history[ pair ] = [[], []] 
                self.state[pair] = {p:{} for p in pair}

    def print_population_performance( self ):
        ''' Helper that prints some information on the populations in the arena.
        '''
        for s in sorted( self.population_count.keys(), key = lambda s: s.char):
            print  "%2s %20s count: %4i cumulative: %8.2f avg. performance: %3.2f" % \
                (s.char, s.name, self.population_count[s], self.population_performance_cumulative[s], self.population_performance[s])

    def add_monitoring_element(self, element):
        element.initialize_arena( self )
        self.__monitoring_elements.append( element )

    @property
    def monitoring_elements( self ):
        return self.__monitoring_elements

    def update_monitoring_elements( self ):
        ''' Update all monitoring elements
        '''
        for m in self.__monitoring_elements:
            m.add_data( self )

    def write_monitoring_elements( self ):
        ''' Call monitoring write functions 
        '''
        for m in self.__monitoring_elements:
            m.write()

    def iterate( self ):
        '''Perform a full iteration of the arena. Run agents, evaluate performance, evolve agents.
        '''
        # Let the agents play
        self.run_agents()
        # Evaluate the outcome
        self.evaluate_performance()
        #self.print_population_performance()
        # Evolve agents in the arena
        self.evolve_arena()
        # Update monitoring elements
        self.update_monitoring_elements()
