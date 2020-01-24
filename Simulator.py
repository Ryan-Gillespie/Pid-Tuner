from PID import PID
from GeneBasic import Population
import random
from wrappers import timer


# generates a randomized pid loop
def genIndividual(dnaLen, geneSet):
    # generate a random individual from the geneSet
    dna = []
    for i in range(3):
        dna.append(round(random.choice(geneSet), 2))
    return dna


class Simulator:
    # simulates a pid loop and returns the time taken to complete it
    def simulatePID(self, dna, target):
        self.pid.kP = dna[0]
        self.pid.kI = dna[1]
        self.pid.kD = dna[2]

        ### TODO Implement this function

        return dna[0] - dna[1] - dna[2]

    # constructor initializes the pid loop, and the population
    def __init__(self):
        self.pid = PID()
        geneSet = [.01*i for i in range(101)]
        self.population = Population(2, self.simulatePID, genIndividual, 3, 2000, geneSet)

    # update the pid settings when they change in the ui
    def updatePIDsettings(self, setPoint, tolerance):
        self.pid.setSetPoint(setPoint)
        self.pid.kTolerance = tolerance

    # get the individual with the best fitness
    def getBest(self):
        return self.population.bestInd()

    # get the average fitness individual
    def getAvg(self):
        return self.population.avg_ind()

    # saves the population to file
    def savePopulation(self, filename):
        with open(filename, 'w') as f:
            for dna in self.population.population:
                f.write('[' + str(dna[0]) + ', ' + str(dna[1]) + ', ' + str(dna[2]) + ']\n')

    # TODO implement load Population
    def loadPopulation(self, filename):
        return None

    # develop the population
    @timer
    def evolvePop(self):
        for i in range(25):
            self.population.evolve(1)
            print(self.population.avg_ind())
            print(self.population.bestInd())


# just a test script, takes about 25 seconds to run
sim = Simulator()
sim.evolvePop()
print('Best Individual: ' + str(sim.getBest()))
sim.savePopulation('test.txt')