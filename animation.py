#Displays simulation animation
from Tkinter import *
from NamingGame import *
from CombinatorialNamingGame import *

def LtoS(l):
    s = ''
    for e in l:
        s += '\n'+e
    return s

def animationNamingGame(agents, meaningInventory):
    
    width = len(meaningInventory)*100+100
    height = len(agents)*100+100

    window = Tk()
    window.geometry(str(width)+'x'+str(height)+"+100+100")
    canvas = Canvas(window)
    canvas.pack(fill=BOTH, expand=10)

    data = {}
    for i in range(len(agents)):
        data[i] = {}
        agentLabel = canvas.create_text(20,100*(i+1)+10,anchor=W,fill="black",text='Agent'+str(i+1),font=('Cambria',18))
    for j in range(len(meaningInventory)):
        objectLabel = canvas.create_text(100*(j+1),20,anchor=W,fill="black",text='Object'+str(j+1),font=('Cambria',18))
    for a in range(len(agents)):
        for o in range(len(meaningInventory)):
            data[a][o] = canvas.create_text(100*(o+1),100*(a+1),anchor=W,fill="blue",text='\nEMPTY')

    ## simulation
    step = 1
    while True:
        time = int(10000/step)
        if time < 100:
            time = 100
        canvas.after(time)
        canvas.update()
        ## selected agent and object
        conversationers = random.sample(agents,2)
        speaker = conversationers[0]
        hearer = conversationers[1]
        aS_i = agents.index(speaker)
        aH_i = agents.index(hearer)
        referent, word = speaker.speak()
        feedback, referent, word = hearer.hear(referent, word)
        speaker.speakFeedback(feedback, referent, word)
        if feedback == True:
            color = "green"
        else:
            color = "red"
        r_i = referent-1
        
        vS = speaker.getVocabulary()
        contentS = LtoS(vS[r_i+1])
        vH = hearer.getVocabulary()
        contentH = LtoS(vH[r_i+1])
        
        canvas.delete(data[aS_i][r_i])
        data[aS_i][r_i] = canvas.create_text(100*(r_i+1),100*(aS_i+1),anchor=W,fill=color,text='SPEAK:'+contentS,font=('Cambria',18))
        canvas.delete(data[aH_i][r_i])
        data[aH_i][r_i] = canvas.create_text(100*(r_i+1),100*(aH_i+1),anchor=W,fill=color,text='HEAR:'+contentH,font=('Cambria',18))
              
        canvas.after(time)
        canvas.update() 
        color = "black"
        canvas.delete(data[aS_i][r_i])
        data[aS_i][r_i] = canvas.create_text(100*(r_i+1),100*(aS_i+1),anchor=W,fill=color,text=contentS,font=('Cambria',18))
        canvas.delete(data[aH_i][r_i])
        data[aH_i][r_i] = canvas.create_text(100*(r_i+1),100*(aH_i+1),anchor=W,fill=color,text=contentH,font=('Cambria',18))

        step+=1


    window.title('Naming Game')
    window.mainloop()

def animationNG():
    numberOfAgent=3
    wordInventory = ['A','B','C','D','E','F','G','H','I','J']
    meaningInventory = [x+1 for x in range(2**3)]
    agents = [NamingAgent(ID, wordInventory, meaningInventory) for ID in range(1,numberOfAgent+1)]
    animationNamingGame(agents, meaningInventory)
    
def animationCNG():
    numberOfAgent=3
    phonemeInventory=['a','b']
    meaningInventory=[x+1 for x in range(2**3)]
    agents = [SimpleCombinatorialNamingAgent(ID, phonemeInventory, meaningInventory) for ID in range(1,numberOfAgent+1)]
    animationNamingGame(agents, meaningInventory)
    
