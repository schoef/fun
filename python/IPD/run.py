#! /usr/bin/env python

#Standard
import random

from arena.AllPairings import AllPairings
from arena.Torus import Torus
from arena.Rectangle import Rectangle
from arena.Line import Line
from arena.Circle import Circle

#Strategies
from strategy.all import * 

# argParser
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--strategies',  action='store', nargs='*',  choices=[s.name for s in strategies], default=['TFT', 'SuspiciousTFT', 'Adaptive', 'Grudger', 'Random'], help="Strategies." )
argParser.add_argument('--size', default=5, action='store', type=int, help = 'size of Arena')
argParser.add_argument('--nmax', default=-1, action='store', type=int, help = 'Maxumim number of iterations')

#argParser.add_argument('--prob', default=0.05, action='store', type=float )

args = argParser.parse_args()

arena = Torus( nx = args.size, ny = args.size)

strategies_in_arena = []
for i_s, s in enumerate(args.strategies):
    base = eval(s)
    tmp = type("CopyOf"+s, (base,), {})
    strategies_in_arena.append( tmp )
    tmp.char = str(i_s)

arena.initialize_random( strategies_in_arena )

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

    if len(set(map(type, arena.agents.values())))==1: 
        print "Converged after %i iterations!" % counter
        break

    if args.nmax>0 and counter>= args.nmax: 
        print "Stopped after %i iterations!" % counter
        break

print
arena.evaluate_performance()
print arena
arena.print_population_performance()
