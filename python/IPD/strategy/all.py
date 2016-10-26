''' Implementation of Iterated Prisoners Dilemma Strategies
'''
#http://www.iterated-prisoners-dilemma.net/prisoners-dilemma-strategies.shtml

#Strategies
from TFT import TFT, TFT_remorse, SuspiciousTFT, TFTT, SuspiciousTFTT, TFTTHybrid
from Random import Random
from Grudger import Grudger
from SoftGrudger import SoftGrudger
from Pavlov import Pavlov
from Adaptive import Adaptive
from Gradual import Gradual
from Defector import Defector
from Cooperator import Cooperator
from Agent import probability_random, probability_defect, probability_cooperate

# Data directory
try:
    probability = sys.modules['__main__'].probability
except:
    probability = 0.05 


NaiveProber      = probability_defect(TFT, probability, char = 'N',  name = 'NaiveProber')
NaivePeacemaker  = probability_cooperate(TFT, probability, char = 'P',  name = 'NaivePeacemaker')
RemorsefulProber = probability_defect(TFT_remorse, probability, char = 'r',  name = 'RemorsefulProber')
TruePeacemaker   = probability_cooperate(TFTTHybrid, probability, char = 'P',  name = 'TruePeacemaker')
PavlovRandom     = probability_random(Pavlov, probability, char = 'P',  name = 'PavlovRandom')

strategies = [ \

# Non-probabilistic
    TFT, SuspiciousTFT, 
    TFTT, SuspiciousTFTT, 
    TFTTHybrid, 
    Grudger, SoftGrudger, Pavlov, Adaptive, Gradual,

# probabilistic derivates
    NaiveProber, RemorsefulProber, NaivePeacemaker, TruePeacemaker, PavlovRandom,

# simple
    Random, Defector, Cooperator 
]
