#! /usr/bin/env python

#Standard
import random

from arena.AllPairings import AllPairings
from arena.Torus import Torus
from arena.Rectangle import Rectangle
from arena.Line import Line
from arena.Circle import Circle

#Strategies
#Strategies
from strategy.TFT import TFT, TFT_SD, TFTT, TFTT_SD
from strategy.Random import Random
from strategy.Defector import Defector
from strategy.Cooperator import Cooperator
from strategy.Agent import probability_random, probability_defect, probability_cooperate

# 'prob' chance to have random behaviour
prob = 0.05
TFT_coopProp   = probability_cooperate(TFT, prob, char = 'T', name = 'TFT(%iC)'%(100*prob))
TFT_defectProp = probability_defect(TFT, prob, char = 'T',  name = 'TFT(%iD)'%(100*prob))
TFT_randProp = probability_random(TFT, prob, char = 'T', name = 'TFT(%iR)'%(100*prob) )

TFT_SD_coopProp   = probability_cooperate(TFT_SD, prob, char = 't', name = 'TFT-D(%iC)'%(100*prob))
TFT_SD_defectProp = probability_defect(TFT_SD, prob, char = 't', name = 'TFT-D(%iD)'%(100*prob))
TFT_SD_randProp = probability_random(TFT_SD, prob, char = 't', name = 'TFT-D(%iR)'%(100*prob))

#arena = Line.fromList([Defector, Cooperator])
#arena = Line.fromList([Defector, Defector])
#arena = Line.fromList([Cooperator, Defector])
#arena = Line.fromList([Cooperator, Cooperator])
#arena = Line.fromList([TFT, TFT_SD])
#arena = Line.fromList([TFT_SD, TFT, TFT_SD])
#arena = Circle.fromList([Cooperator, TFT_SD, TFT, TFT_SD, TFT, Cooperator])

#arena = Circle( n = 100 )
#arena.initialize_random( strategies = [TFT,  TFT_coopProp, TFT_defectProp] )
#arena = AllPairings( n = 10 )
#arena.initialize_random( strategies = [TFT,  TFT_coopProp, TFT_defectProp] )

arena = Torus( nx = 5, ny = 5)
#arena = Torus( nx = 15, ny = 15)
strategies = [TFT_SD_randProp, TFT_randProp]
#strategies = [TFT_SD, TFT]
arena.initialize_random( strategies = strategies )

#population = [ random.choice([ TFT, Random]) for i in range(10)]
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
