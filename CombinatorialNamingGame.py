## add a phonemic combination feature into the Naming Game
## inventing new word by adding an addition phoneme to a word randomly picked out of his word inventory.

from pylab import *
import random
from NamingGame import *
from utils import *
from SocialStructure import *

class SimpleCombinatorialNamingAgent(NamingAgent):

    def __init__(self, ID=0, phonemeInventory=[], meaningInventory=[]):
        self.name = 'Agent'+str(ID)
        self.v = {} # vocabulary
        self.pI = phonemeInventory
        self.wI = phonemeInventory # wordInventory initially the same as phonemeInventory
        self.mI = meaningInventory
        self.h = [] # interacting history

    def inventWord(self, referent):
        pool = setdiff(self.wI,unique(deepvalues(self.v)))
        if pool == []:
            word = random.choice(self.wI)+random.choice(self.pI)
            while word in unique(deepvalues(self.v)):
                word = random.choice(self.wI)+random.choice(self.pI)
            self.v[referent] = [word]
            self.wI.append(word)
        else:
            self.v[referent] = [random.choice(pool)] ## avoid using used word

class SimpleCombinatorialNamingGame():

    def __init__(self, numberOfAgent=2, phonemeInventory=['a','b'],meaningInventory=range(2**3),graph='complete'):
        self.agents = [SimpleCombinatorialNamingAgent(ID, phonemeInventory, meaningInventory) for ID in range(1,numberOfAgent+1)]
        self.phonemeInventory = phonemeInventory
        self.meaningInventory = meaningInventory
        self.Hs = [] ## communication results history,list of True or False
        self.successRates = []
        if graph == 'complete':
            self.Graph = Complete(numberOfAgent)
        elif graph == 'tree':
            self.Graph = Tree(numberOfAgent)
        elif graph == 'circle':
            self.Graph = Circle(numberOfAgent)
        elif graph == 'path':
            self.Graph = Path(numberOfAgent)
        elif graph == 'scalefree':
            self.Graph = Barabasi(numberOfAgent)
        else:
            print 'invalid social structure for agents'

    def dialog(self):
        conversationers = choose(self.agents,self.Graph) 
        speaker = conversationers[0]
        hearer = conversationers[1]
        referent, word = speaker.speak()
        feedback, referent, word = hearer.hear(referent, word)
        speaker.speakFeedback(feedback, referent, word)
        self.Hs.append(feedback)
        self.successRates.append(sum(self.Hs)/float(len(self.Hs)))

    def dialogGivenTime(self,timeSteps=10000):
        for i in range(timeSteps):
            self.dialog()

    def dialogTilConverge(self,epsilon=0.05):
        t = 1
        self.dialog()
        while 1-self.successRates[-1]>epsilon:
            self.dialog()
            t+=1
        return t

    def outputVocabulary(self):
        Vs = [agent.getVocabulary() for agent in self.agents]
        names = [agent.getName() for agent in self.agents]
        for i in range(len(names)):
            print names[i],'\t',[Vs[i][k] for k in self.meaningInventory]

    def plotSuccessRates(self):
        plot(self.successRates)
        ylabel('Success Rate');xlabel('TimeStep')
        show()

    def countHomophones(self):
        Vs = [agent.getVocabulary() for agent in self.agents]
        l = [Vs[1][k] for k in self.meaningInventory]
        return countHomophones(l)
        

def homophones_time_popSize_pIsize(pIRange=[2,4,8,16],populationRange=[2,4,8,16,32],gameSteps=50):
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    with open('results/popSize_pIsize_homophones_time.txt','w') as f:
        f.write('pIsize\tpopSize\tnumHomophones\ttimeForConvergence\n')
        for p in pIRange:
            pI = alphabet[0:p]
            for n in populationRange:
                homophoneSize = []
                timeTilConverge = []
                for i in range(gameSteps):
                    game = SimpleCombinatorialNamingGame(n,phonemeInventory=pI)
                    timeTilConverge.append(game.dialogTilConverge(0.1))
                    homophoneSize.append(game.countHomophones())
                    print 'gameStep ',i+1,'...'
                    print '(population size:',n,'; pIsize:',p,'; number of homophones:', homophoneSize[-1],'; time used:', timeTilConverge[-1],')'
                    line = str(p)+'\t'+str(n)+'\t'+str(homophoneSize[-1])+'\t'+str(timeTilConverge[-1])+'\n'
                    f.write(line)
                game.outputVocabulary()
            
##    ## plot
##    figure(figsize=(16,8))
##    subplot(121);title('Time Needed for Convergence')
##    plot(T)
##    xlabel('Population Size');ylabel('Time')
##    subplot(122);title('Number of Homophones')
##    plot(H)
##    xlabel('Population Size');ylabel('Number of Homophones')
##    show()

def homophones_time_popSize_socStr(socialStructures=['complete','tree','scalefree','circle','path'],populationRange=[2,4,8,16,32,64],gameSteps=50):
    with open('results/popSize_socStr_homophones_time.txt','w') as f:
        f.write('socStr\tpopSize\tnumHomophones\ttimeForConvergence\n')
        for socStr in socialStructures:
            for n in populationRange:
                homophoneSize = []
                timeTilConverge = []
                for i in range(gameSteps):
                    game = SimpleCombinatorialNamingGame(n,graph=socStr)
                    timeTilConverge.append(game.dialogTilConverge(0.1))
                    homophoneSize.append(game.countHomophones())
                    print 'gameStep ',i+1,'...'
                    print '(population size:',n,'; social structure:',socStr,'; number of homophones:', homophoneSize[-1],'; time used:', timeTilConverge[-1],')'
                    line = str(socStr)+'\t'+str(n)+'\t'+str(homophoneSize[-1])+'\t'+str(timeTilConverge[-1])+'\n'
                    f.write(line)
                game.outputVocabulary()

def run():
    homophones_time_popSize_pIsize()
    homophones_time_popSize_socStr()
