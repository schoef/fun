#! /usr/bin/env python

# Standard
import random
import os
import signal
import sys

# Arenas
from arena.AllPairings import AllPairings
from arena.Torus import Torus
from arena.Rectangle import Rectangle
from arena.Line import Line
from arena.Circle import Circle

# Strategies
from strategy.all import * 

# Monitoring
from monitoring.PopulationFractions import PopulationFractions

# argParser
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--strategies',  action='store', nargs='*',  choices=[s.name for s in strategies], default=['TFT', 'TFTT', 'Random'], help="Strategies." )
argParser.add_argument('--arena',  action='store', type=str, default='Torus', choices = ['Torus', 'Rectangle', 'Line', 'Circle', 'AllPairings'], help="Output directory." )
argParser.add_argument('--size', default=20, action='store', type=int, help = 'size of Arena')
argParser.add_argument('--nmax', default=1000, action='store', type=int, help = 'Maximum number of iterations')
argParser.add_argument('--output',  action='store', type=str, default='/Users/robertschoefbeck/Desktop/', help="Output directory." )

#argParser.add_argument('--prob', default=0.05, action='store', type=float )

args = argParser.parse_args()
if args.arena == 'Torus':
    arena = Torus( nx = args.size, ny = args.size)
elif args.arena == 'Rectangle':
    arena = Rectangle( nx = args.size, ny = args.size)
elif args.arena == 'Line':
    arena = Line( n = args.size) 
elif args.arena == 'Circle':
    arena = Circle( n = args.size) 
elif args.arena == 'AllPairings':
    arena = AllPairings( n = args.size)
else:
    raise ValueError( "Don't know about arena %s." % args.arena )


arena.add_monitoring_element( PopulationFractions( filename = os.path.join( args.output, 'PopulationFractions.pdf') ) )

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

def SIGINT_handler(signal, frame):
    print('You pressed Ctrl+C! Writing monitor elements, then stop.')

    # Write result
    arena.write_monitoring_elements()
    print "Bye."
    sys.exit( 0 )

# signal.signal(signal.SIGINT, SIGINT_handler)
#print('Press Ctrl+C')
#signal.pause()

while True:
    try:
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
    except KeyboardInterrupt:
        print "Bye."
        arena.write_monitoring_elements()
        sys.exit()
print
arena.evaluate_performance()
print arena
arena.print_population_performance()

# Write result
arena.write_monitoring_elements()
