#! /usr/bin/env python

#Standard
import random

from arena.AllPairings import AllPairings
from arena.Torus import Torus
from arena.Rectangle import Rectangle
from arena.Line import Line
from arena.Circle import Circle

#Strategies
from strategy.TFT import TFT_start_cooperate, TFT_start_defect
from strategy.Random import Random
from strategy.Defector import Defector
from strategy.Cooperator import Cooperator
from strategy.Agent import probability_random, probability_defect, probability_cooperate

# 'prob' chance to have random behaviour
prob = 0.05
TFT_start_cooperate_coopProp   = probability_cooperate(TFT_start_cooperate, prob, char = 'T', name = 'TFT(%iC)'%(100*prob))
TFT_start_cooperate_defectProp = probability_defect(TFT_start_cooperate, prob, char = 'T',  name = 'TFT(%iD)'%(100*prob))
TFT_start_cooperate_randProp = probability_random(TFT_start_cooperate, prob, char = 'T', name = 'TFT(%iR)'%(100*prob) )

TFT_start_defect_coopProp   = probability_cooperate(TFT_start_defect, prob, char = 't', name = 'TFT-D(%iC)'%(100*prob))
TFT_start_defect_defectProp = probability_defect(TFT_start_defect, prob, char = 't', name = 'TFT-D(%iD)'%(100*prob))
TFT_start_defect_randProp = probability_random(TFT_start_defect, prob, char = 't', name = 'TFT-D(%iR)'%(100*prob))

#arena = Line.fromList([Defector, Cooperator])
#arena = Line.fromList([Defector, Defector])
#arena = Line.fromList([Cooperator, Defector])
#arena = Line.fromList([Cooperator, Cooperator])
#arena = Line.fromList([TFT_start_cooperate, TFT_start_defect])
#arena = Line.fromList([TFT_start_defect, TFT_start_cooperate, TFT_start_defect])
#arena = Circle.fromList([Cooperator, TFT_start_defect, TFT_start_cooperate, TFT_start_defect, TFT_start_cooperate, Cooperator])

#arena = Circle( n = 100 )
#arena.initialize_random( strategies = [TFT_start_cooperate,  TFT_start_cooperate_coopProp, TFT_start_cooperate_defectProp] )
#arena = AllPairings( n = 10 )
#arena.initialize_random( strategies = [TFT_start_cooperate,  TFT_start_cooperate_coopProp, TFT_start_cooperate_defectProp] )

arena = Torus( nx = 5, ny = 5)
#arena = Torus( nx = 15, ny = 15)
strategies = [TFT_start_defect_randProp, TFT_start_cooperate_randProp]
#strategies = [TFT_start_defect, TFT_start_cooperate]
arena.initialize_random( strategies = strategies )

#population = [ random.choice([ TFT_start_cooperate, Random]) for i in range(10)]
#strategies = list(set(population))
#arena = Line.fromList( population )

counter = 0
print "Start with"
print arena
print
while True:
    print "At", counter
    arena.iterate()
    counter += 1
    print arena
    arena.print_population_performance()
    if len(set(map(type, arena.agents.values())))==1: break

print
print "Converged after %i iterations!" % counter
arena.evaluate_performance()
print arena
arena.print_population_performance()
