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
    #self has to be called first and is not needed to class an instance of the class
    def _init_(self, initial, final):
        #self.initial/final is the class var after = is the local var
        self.initial=initial
        self.final=final

#populate using the result of the shunting yard algroithm
def compile(postfix):
    nfaStack = []
    for c in postfix:
        #creating a new instance of the state class
        accept = state()
        initial= state()
        initial.label = c

print('WORKS')