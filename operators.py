from pyevolve.GSimpleGA import *

class DCGSimpleGA(GSimpleGA):
    def __init__(self, *args, **kwargs):
        GSimpleGA.__init__(self, *args, **kwargs)

    def step(self):
        """ Just do one step in evolution, one generation """
        genomeMom = None
        genomeDad = None

        newPop = GPopulation(self.internalPop)
        logging.debug("Population was cloned.")

        size_iterate = len(self.internalPop)

        # Odd population size
        if size_iterate % 2 != 0: size_iterate -= 1

        crossover_empty = self.select(popID=self.currentGeneration).crossover.isEmpty()

        for i in xrange(0, size_iterate, 2):
            genomeMom = self.select(popID=self.currentGeneration)
            genomeDad = self.select(popID=self.currentGeneration)

            if not crossover_empty and self.pCrossover >= 1.0:
                for it in genomeMom.crossover.applyFunctions(mom=genomeMom, dad=genomeDad, count=2):
                    (sister, brother) = it
            else:
                if not crossover_empty and Util.randomFlipCoin(self.pCrossover):
                    for it in genomeMom.crossover.applyFunctions(mom=genomeMom, dad=genomeDad, count=2):
                        (sister, brother) = it
                else:
                    sister = genomeMom.clone()
                    brother = genomeDad.clone()

            sister.mutate(pmut=self.pMutation, ga_engine=self)
            brother.mutate(pmut=self.pMutation, ga_engine=self)

            newPop.internalPop.append(sister)
            newPop.internalPop.append(brother)

        if len(self.internalPop) % 2 != 0:
            genomeMom = self.select(popID=self.currentGeneration)
            genomeDad = self.select(popID=self.currentGeneration)

            if Util.randomFlipCoin(self.pCrossover):
                for it in genomeMom.crossover.applyFunctions(mom=genomeMom, dad=genomeDad, count=1):
                    (sister, brother) = it
            else:
                sister = random.choice([genomeMom, genomeDad])
                sister = sister.clone()
                sister.mutate(pmut=self.pMutation, ga_engine=self)

            newPop.internalPop.append(sister)

        logging.debug("Evaluating the new created population.")
        newPop.evaluate()

        # Niching methods- Petrowski's clearing
        self.clear()

        if self.elitism:
            logging.debug("Doing elitism.")
            if self.getMinimax() == Consts.minimaxType["maximize"]:
                for i in xrange(self.nElitismReplacement):
                    if self.internalPop.bestRaw(i).score > newPop.bestRaw(i).score:
                        newPop[len(newPop) - 1 - i] = self.internalPop.bestRaw(i)
            elif self.getMinimax() == Consts.minimaxType["minimize"]:
                for i in xrange(self.nElitismReplacement):
                    if self.internalPop.bestRaw(i).score < newPop.bestRaw(i).score:
                        newPop[len(newPop) - 1 - i] = self.internalPop.bestRaw(i)

        self.internalPop = newPop
        self.internalPop.sort()

        logging.debug("The generation %d was finished.", self.currentGeneration)

        self.currentGeneration += 1

        return (self.currentGeneration == self.nGenerations)
