from Action import Action

class ActionNode:
    parent = None
    branches = []
    action = None
    badAction = False
    
    def __init__(self, parent=None, action=None):
        self.branches = []
        self.parent = parent
        self.action = action

    #create parented branch
    def newBranch(self, action):
        self.branches.append(ActionNode(self, action))

    #finds the next available branch
    def nextAvailable(self):
        for b in self.branches:
            if (b.badAction == False):
                return b
        if(self.parent!=None):
            return self.parent.nextAvailable()
    #clears further branches
    def clear(self):
        self.branches = []
    
    #returns head of the tree
    def head(self):
        if(self.parent!=None):
            p = None
            while(self.parent!=None):
                p = self.parent
            return self.parent
        return self
    

        




#class ActionTree(ActionNode):
#    def clear:

