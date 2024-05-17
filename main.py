import time

import pyautogui
from ActionTree import ActionNode
from game_logic import GameLogic
from game_ui import GameUI

time.sleep(10)
print("waited")

gl = GameLogic()
gui = GameUI()
gui.focusOnEmulatorScreen()

def DrawLoop():
        i=0
        while(i<=24):
            gui.Draw()
            i+=1
            '''
            x=gl.PlaceAce(gui.gs)
            if(x!=None):
                next_action, y = x
                gui.ProcessAction(next_action)
            '''
            

DrawLoop()
tree=ActionNode()
last_action=None

#print('test')
try:
    while 1:
        #finds current card locations
        print("Updating Game State")
        gui.UpdateGameState()
    
        #evaluates next move option
        print("Calculating Action")
        next_action = gl.GetNextAction(gui.gs, gui.gv)
        #if(last_action==next_action):
        #    break

        #print("Action: " + next_action.name)
        #print(next_action.cards)
    
        #inpstr = input('Continue?')
        #if inpstr != "y":
        #    exit(0)

        #acts on the current move
        gui.ProcessAction(next_action)
        last_action=next_action

        #time.sleep(1)
        #exit(0)
except: KeyboardInterrupt

    