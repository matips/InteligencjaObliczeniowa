# $Id: pyevolve_ex3_schaffer.py 150 2009-01-18 19:29:13Z christian.perone $

import numpy as np
from pyevolve import G1DList, GSimpleGA
from pyevolve import Initializators, Consts
# import matplotlib.pyplot as plt
# This is the Schaffer F6 Function, a deceptive function
from pyevolve.Crossovers import G1DListCrossoverSinglePoint
from pyevolve.Mutators import G1DListMutatorRealGaussian
from pyevolve.Selectors import GRouletteWheel
from graphs import visual
from operators import DCGSimpleGA


def schafferF6(xlist):
    t1 = np.sin(np.sqrt(xlist[0] * xlist[0] + xlist[1] * xlist[1]));
    t2 = 1 + 0.001 * (xlist[0] * xlist[0] + xlist[1] * xlist[1]);
    score = 0.5 + (t1 * t1 - 0.5) / (t2 * t2)
    return score


def runAlghoritm(AlghoritmClass, name= ""):
    genome = G1DList.G1DList(2)
    genome.setParams(rangemin=-10, rangemax=10, bestrawscore=0.00, roundDecimal=8)
    genome.initializator.set(Initializators.G1DListInitializatorReal)
    genome.mutator.set(G1DListMutatorRealGaussian)
    genome.crossover.set(G1DListCrossoverSinglePoint)
    # The evaluator function (objective function)
    genome.evaluator.set(schafferF6)

    # Genetic Algorithm Instance
    ga = AlghoritmClass(genome)
    ga.selector.set(GRouletteWheel)

    ga.minimax = Consts.minimaxType["minimize"]
    ga.setGenerations(400)
    ga.setMutationRate(0.15)
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
    populationDC = runAlghoritm(DCGSimpleGA, "DC")
    standardPopulation = runAlghoritm(GSimpleGA.GSimpleGA, "standard")

    visual(schafferF6, [{
        'individuals': populationDC,
        'style': 'or',
        'name': "DC"
    }, {
        'individuals': standardPopulation,
        'style': 'ob',
        'name': "standard"
    }])
