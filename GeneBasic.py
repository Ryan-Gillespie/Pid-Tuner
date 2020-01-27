from wrappers import roundAll
import random

class Population:
    def __init__(self, target, fit, ind, dnaLen, popSize, geneSet):
        self.target = target
        self.fit = fit
        self.ind = ind
        self.dnaLen = dnaLen
        self.popSize = popSize
        self.geneSet = geneSet

        self.mutationChance = .1

        self.genPopulation()

    def genPopulation(self):
        population = []
        for i in range(self.popSize):
            population.append(self.ind(self.dnaLen, self.geneSet))
        self.population = population

    def weighted_population(self):
        best = 0
        self.weightedPop = []
        for individual in self.population:
            try:
                weight = 1 / abs((self.target - self.fit(individual, self.target)) / self.target)
            except ZeroDivisionError:
                weight = 100
            if (weight > best):
                best = weight
                self.best = individual
            self.weightedPop.append([individual, weight])
        return self.weightedPop

    def weighted_choice(self, items):
        weight_total = sum((item[1] for item in items))
        n = random.uniform(0, weight_total)
        for item, weight in items:
            if n < weight:
                return item
            n = n - weight
        return item

    def createChildren(self, dna1, dna2):
        pos = int(random.random() * self.dnaLen)
        return (dna1[:pos] + dna2[pos:], dna2[:pos] + dna1[pos:])

    def randomFromGeneSet(self):
        pos = int(random.random() * len(self.geneSet))
        return self.geneSet[pos]

    def mutate(self, individual):
        for i in range(len(individual)):
            if (random.random() * self.mutationChance == 1):
                individual[i] = self.randomFromGeneSet()
        return individual

    # it says avg but its really the median
    def avg_ind(self):
        ind = sorted(self.weighted_population(), key=lambda x: x[1])[int(self.popSize/2)]
        return [ind[0], self.fit(ind[0], self.target)]

    # get the best individual (highest weight)
    def bestInd(self):
        if self.best is None:
            ind = sorted(self.weighted_population(), key=lambda x: x[1], reverse=True)[0]
            return [ind[0], self.fit(ind[0], self.target)]
        else:
            return [self.best, self.fit(self.best, self.target)]

    def evolve(self, iterations):
        for i in range(iterations):
            wPop = self.weighted_population()
            self.population = []
            for x in range(int(self.popSize / 2)):
                ind1 = self.weighted_choice(wPop)
                ind2 = self.weighted_choice(wPop)

                ind1, ind2 = self.createChildren(ind1, ind2)

                self.population.append(self.mutate(ind1))
                self.population.append(self.mutate(ind2))

    def __str__(self):
        best = self.bestInd()
        return str([round(val, 3) for val in best[0]]) + ': ' + str(best[1])
