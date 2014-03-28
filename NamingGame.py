## a minimal form of Naming Game, based on Baronchelli et al. 2006

from pylab import *
import random
from utils import *

class NamingAgent(object):
    
    def __init__(self, ID=0, wordInventory=[], meaningInventory=[]):
        self.name = 'Agent'+str(ID)
        self.v = {} # vocabulary
        self.wI = wordInventory
        self.mI = meaningInventory
        self.h = [] # interacting history, True = success dialog, False = failed dialog

    def getVocabulary(self):
        return self.v

    def getName(self):
        return self.name

    def getHistory(self):
        return self.h

    def inventWord(self, referent):
        pool = setdiff(self.wI,unique(deepvalues(self.v)))
        self.v[referent] = [random.choice(pool)]

    def speak(self):
        referent = random.choice(self.mI)
        if referent not in self.v:
            self.inventWord(referent)
        return referent, random.choice(self.v[referent])

    def hear(self, referent, word):
        if referent not in self.v:
            self.v[referent] = [word]
            self.h += [False]
            if word not in self.wI:
                self.wI.append(word)
        else:
            if word not in self.v[referent]:
                self.v[referent] += [word]
                self.h += [False]
                if word not in self.wI:
                    self.wI.append(word)
            else:
                self.v[referent] = [word]
                self.h += [True]
                if word not in self.wI:
                    self.wI.append(word)
        return self.h[-1], referent, word

    def speakFeedback(self, feedback, referent, word):
        if feedback == True:
            self.v[referent] = [word]
            self.h += [True]
        else:
            self.h += [False]

def NamingGame():
    ## intialize
    wordInventory = ['Abc','Bcd','Cde','Def','Efg']
    meaningInventory = [1,2,3,4]
    agents = [NamingAgent(ID, wordInventory, meaningInventory) for ID in range(1,6)]
    timeSteps = 1000
    
    ## dialog
    Hs = []
    for i in range(timeSteps):
        conversationers = random.sample(agents,2)
        speaker = conversationers[0]
        hearer = conversationers[1]
        referent, word = speaker.speak()
        feedback, referent, word = hearer.hear(referent, word)
        speaker.speakFeedback(feedback, referent, word)
        Hs.append(feedback)
    
    ## output
    Vs = [agent.getVocabulary() for agent in agents]
    names = [agent.getName() for agent in agents]
    successRates = []
    for i in range(len(names)):
        print names[i], [Vs[i][k] for k in meaningInventory]
    for j in range(1,timeSteps+1):
        successRates.append(sum(Hs[0:j])/float(j))
    plot(successRates)
    ylabel('Success Rate');xlabel('TimeStep')
    show()
