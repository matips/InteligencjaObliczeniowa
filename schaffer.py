# $Id: pyevolve_ex3_schaffer.py 150 2009-01-18 19:29:13Z christian.perone $
from math import pi

import numpy as np
import sys
from pyevolve import G1DList, GSimpleGA
from pyevolve import Initializators, Consts
# import matplotlib.pyplot as plt
# This is the Schaffer F6 Function, a deceptive function
from pyevolve.Mutators import G1DListMutatorRealGaussian
from pyevolve.Selectors import GRouletteWheel
from graphs import visual
from operators import DCGSimpleGA, G1DListCrossoverBetweenPoint


def schafferF6(xlist):
    t1 = np.sin(np.sqrt(xlist[0] * xlist[0] + xlist[1] * xlist[1]));
    t2 = 1 + 0.001 * (xlist[0] * xlist[0] + xlist[1] * xlist[1]);
    score = 0.5 + (t1 * t1 - 0.5) / (t2 * t2)
    return score


def rastrigin(xlist):
    x1 = xlist[0]
    x2 = xlist[1]
    # return x1 * x1 - 10 * np.cos(2 * np.pi * x1) + x2 * x2 - 10 * np.cos(2 * np.pi * x2) + 2 * 10
    return sum([x * x - 10 * np.cos(2 * np.pi * x) for x in xlist]) + 20


def runAlghoritm(AlghoritmClass, name="", function=schafferF6, steps=100):
    genome = G1DList.G1DList(2)
    genome.setParams(rangemin=-20, rangemax=10, bestrawscore=0.00, roundDecimal=8)
    genome.initializator.set(Initializators.G1DListInitializatorReal)
    genome.mutator.set(G1DListMutatorRealGaussian)
    genome.crossover.set(G1DListCrossoverBetweenPoint)
    # The evaluator function (objective function)
    genome.evaluator.set(function)

    # Genetic Algorithm Instance
    ga = AlghoritmClass(genome)
    ga.selector.set(GRouletteWheel)

    ga.minimax = Consts.minimaxType["minimize"]
    ga.setGenerations(steps)
    ga.setMutationRate(0.6)
    # ga.setPopulationSize(200)
    ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)

    # Do the evolution, with stats dump
    # frequency of 10 generations
    ga.evolve(freq_stats=100)

    # Best individual
    best = ga.bestIndividual()
    print "\nBest individual score for %s: %.2f\n\n\n" % (name, best.score,)
    # print "\n".join(map(
    #     lambda individual: str({
    #         'x': individual.genomeList[0],
    #         'y': individual.genomeList[1],
    #         'score': individual.score
    #     }),
    #     sorted(ga.getPopulation(), key=lambda el: el.score)
    # ))
    return ga.getPopulation()


if __name__ == "__main__":
    # Genome instance
    funtion_name = sys.argv[1]

    function = {'rastrigin': rastrigin, 'schafferF6': schafferF6}.get(sys.argv[1])
    steps = int(sys.argv[2])
    populationDC = runAlghoritm(DCGSimpleGA, "DC", function=function, steps=steps)
    standardPopulation = runAlghoritm(GSimpleGA.GSimpleGA, "standard")

    visual(function, [{
        'individuals': populationDC,
        'style': 'oy',
        'name': "DC"
    }, {
        'individuals': standardPopulation,
        'style': 'ko',
        'name': "standard"
    }], steps=steps)
