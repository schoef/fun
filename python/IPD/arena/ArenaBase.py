''' Base class for an arena where Agents play IPD 
'''

#Helpers
from helpers.PrisonerDilemma import PrisonerDilemma

import abc
import random

class ArenaBase:
    __metaclass__ = abc.ABCMeta
    
    def __init__( self ):
        ''' Initialize the ArenaBase 
        '''
        assert hasattr( self, "positions"), "Class that derives from ArenaBase must define positions"
   
        # Initialize empty history 
        self.pairs   = list( set ( [ tuple(sorted( (p, q) )) for p in self.positions for q in self.neighbours( p ) ] ))
        self.history = { pair:[[],[]] for pair in self.pairs }
        self.max_history_length = 5        
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

    def run_agents( self ):
        ''' Let all player pairs play, increment the agents revenues and add result to history
        '''
        self.agent_revenue = {p:0. for p in self.positions}
        self.agent_neighbour_count   = {p:0. for p in self.positions}
        for pair in self.pairs:
            a1, a2 = pair

            # Play!
            decision_agent1 = self.agents[a1]( self.history[pair] )
            decision_agent2 = self.agents[a2]( list(reversed(self.history[pair])) )

            revenue_agent1, revenue_agent2 = PrisonerDilemma.revenue( decision_agent1, decision_agent2 )

            # Increment revenue and count of games
            self.agent_revenue[a1] += revenue_agent1
            self.agent_revenue[a2] += revenue_agent2
            self.agent_neighbour_count[a1]   += 1
            self.agent_neighbour_count[a2]   += 1

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
        self.agent_performance = {p:self.agent_revenue[p]/self.agent_neighbour_count[p] for p in self.positions}

        # Accumulating results per strategy
        self.population_performance_cumulative    = {}
        self.population_count          = {}
        for p in self.positions:
            strategy = type(self.agents[p])
            if strategy not in self.population_performance_cumulative.keys():
                self.population_performance_cumulative[strategy]  = self.agent_performance[p]
                self.population_count[strategy]        = 1
            else:
                self.population_performance_cumulative[strategy]  += self.agent_performance[p]
                self.population_count[strategy]        += 1

        # Averaging strategy performance
        self.population_performance = {}
        for strategy in self.population_performance_cumulative.keys():
            self.population_performance[strategy] = self.population_performance_cumulative[strategy]/self.population_count[strategy]

    def evolve_agents( self ):
        '''Evolve agents based on the agents performance.
        An agent is removed if all neighbours perform better. 
        It is replaced by a random choice among the neighbours with the best performance.
        Histories of the affected pairs are reset.
        '''
        
        replacements = []
        for p in self.positions:
            neighbour_performances = {q:self.agent_performance[q] for q in self.neighbours( p )}
            # find local performance minima
            if all( self.agent_performance[p] < performance for performance in neighbour_performances.values()):
                # find best performing neighbour strategies
                maximum_performance = max(neighbour_performances.values())
                winners = [type(self.agents[q]) for q in neighbour_performances.keys() if self.agent_performance[q]==maximum_performance] 
                # select random winner if multiple strategies
                #print agent_performance[p], maximum_performance, neighbour_performances.values(), winners
                if len(winners)>1:
                    winner = winners[ random.randrange(0, len(winners)) ] 
                else:
                    winner = winners[0]
                replacements.append( (p, winner) )

        # Replace looser with winner instance and delete history with neighbours
        for pos, winner in replacements:
            if type(self.agents[pos]) == winner:
                continue

            #print "Replacing %r with %r" % ( type(self.agents[pos]), winner) 

            self.agents[pos] = winner()
            for q in self.neighbours( p ):
                self.history[ tuple(sorted(( p, q ))) ] = [[], []] 

    def print_population_performance( self ):
        for s in self.population_count.keys():
            print  "%2s %20s count %i cum %6.2f perf %3.2f" % (s.char, s.name, self.population_count[s], self.population_performance_cumulative[s], self.population_performance[s])

    def iterate( self ):
        '''Perform a full iteration of the arena. Run agents, evaluate performance, evolve agents.
        '''
        self.run_agents()
        self.evaluate_performance()
        #self.print_population_performance()
        self.evolve_agents()
