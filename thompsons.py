#Thompson's Construction
#Aaron Burns

#No modifiers for classes in python
class state:
    #Value None means you don't want to set a value yet
    label = None
    edge1 = None
    edge2 = None

#When declaring an instance of a class
class NFA: 
    initial = None
    final = None

    #Constructor for the NFA class
    #self references the current instance of the class
    #self has to be called first and is not needed to create an instance of the class
    def _init_(self, initial, final):
        #self.initial/final is the class var after = is the local var
        self.initial=initial
        self.final=final

#populate using the result of the shunting yard algroithm
def compile(postfix):
    nfaStack = []
    #for creating an nfa fragment for a non special character
    for c in postfix:
        #creating a new instance of the state class
        accept = state()
        initial= state()
        #the state is called whatever character is read in
        initial.label = c
        #connects the initial state to the accept state
        initial.edge1 = accept
        #edge2 is not needed for the initial state because its the first state
        #create a new NFA object and puts it on the nfa stack
        #the initial state above and the accept state are used by the 
        #nfa constructor to create an nfa for a non special character
        nfaStack.append(NFA(initial, accept))
print('WORKS')