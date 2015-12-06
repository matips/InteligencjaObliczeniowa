# $Id: pyevolve_ex3_schaffer.py 150 2009-01-18 19:29:13Z christian.perone $
import sys

import numpy as np
from pyevolve import G1DList, GSimpleGA
from pyevolve import Initializators, Consts
# import matplotlib.pyplot as plt
import math
# This is the Schaffer F6 Function, a deceptive function
from pyevolve.Mutators import G1DListMutatorRealGaussian
from pyevolve.Selectors import GRouletteWheel

from colorbar import visual
from operators import DCGSimpleGA



def schafferF6(xlist):
    t1 = np.sin(np.sqrt(xlist[0] * xlist[0] + xlist[1] * xlist[1]));
    t2 = 1 + 0.001 * (xlist[0] * xlist[0] + xlist[1] * xlist[1]);
    score = 0.5 + (t1 * t1 - 0.5) / (t2 * t2)
    return score

if __name__ == "__main__":
    # Genome instance
    genome = G1DList.G1DList(2)
    genome.setParams(rangemin=-100, rangemax=100, bestrawscore=0.00, roundDecimal=2)
    genome.initializator.set(Initializators.G1DListInitializatorReal)
    genome.mutator.set(G1DListMutatorRealGaussian)
    # The evaluator function (objective function)
    genome.evaluator.set(schafferF6)

    # Genetic Algorithm Instance
    ga = DCGSimpleGA(genome)
    ga.selector.set(GRouletteWheel)

    ga.minimax = Consts.minimaxType["minimize"]
    ga.setGenerations(1500)
    ga.setMutationRate(0.05)
    ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)

    # Do the evolution, with stats dump
    # frequency of 10 generations
    ga.evolve(freq_stats=100)

    # Best individual
    best = ga.bestIndividual()
    print "\nBest individual score: %.2f\n\n\n" % (best.score,)
    # print "\n".join(map(
    #     lambda individual: str({
    #         'x': individual.genomeList[0],
    #         'y': individual.genomeList[1],
    #         'score': individual.score
    #     }),
    #     sorted(ga.getPopulation(), key=lambda el: el.score)
    # ))
    visual(schafferF6, ga.getPopulation())
