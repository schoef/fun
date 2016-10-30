#! /usr/bin/env python

# Standard imports
import copy

# Arena
from arena.Line import Line

# Strategies
from strategy.all import * 

# argParser
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--strategies',  action='store', nargs=2,  choices=[s.name for s in strategies], default=['Adaptive', 'Random'], help="Strategies." )
argParser.add_argument('--n', default=100, action='store', type=int )
#argParser.add_argument('--prob', default=0.05, action='store', type=float )

args = argParser.parse_args()

arena = Line.fromList( [eval(s) for s in args.strategies] )
assert len(arena.pairs)==1, "Something not right. Can have just one pair in the arena."

a1, a2 = arena.pairs[0]

rev_str = {a:'' for a in arena.agents}
dec_str = {a:'' for a in arena.agents}
rev     = {a:0 for a in arena.agents}
for i in range( args.n ):
    arena.run_agents()
    rev_str[a1]+=str(int(arena.agent_revenue[a1]))
    dec_str[a1]+= ('C' if arena.history[(a1,a2)][0][-1] else 'D')
    rev[a1] += arena.agent_revenue[a1] 
    rev_str[a2]+=str(int(arena.agent_revenue[a2]))
    dec_str[a2]+= ('C' if arena.history[(a1,a2)][1][-1] else 'D')
    rev[a2] += arena.agent_revenue[a2] 
    

print " "*30 + "%s"%(dec_str[a1] )
print "%26s %2s %s"%(arena.agents[a1].name, arena.agents[a1].char, rev_str[a1] )
print "%26s %2s %s"%(arena.agents[a2].name, arena.agents[a2].char, rev_str[a2] )
print " "*30 + "%s"%(dec_str[a2] )

print "Cumulative: %10s %4i (%3.2f), %10s %4i (%3.2f)" % (arena.agents[a1].name, rev[a1], rev[a1]/float(args.n), arena.agents[a2].name, rev[a2], rev[a2]/float(args.n))
