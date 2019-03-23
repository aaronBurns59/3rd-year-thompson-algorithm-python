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
    accept = None
    #Constructor for the NFA class
    #self references the current instance of the class
    #self has to be called first and is not needed to create an instance of the class
    def _init_(self, initial, accept):
        #self.initial/accept is the class var after = is the local var
        self.initial=initial
        self.accept=accept

#populate using the result of the shunting yard algroithm
def compile(postfix):
    nfaStack = []
    #for creating an nfa fragment for a non special character
    for c in postfix:
        if c == '.':
            #stacks are LIFO 
            nfa2= nfaStack.pop()
            nfa1= nfaStack.pop()
            #combine the two states together
            nfa1.accept.edge1 = nfa2.initial
            #Create a new NFA using new intial and accept states
            newNFA = NFA(nfa1.initial, nfa2.accept)
            #push a new nfa onto the stack that is a combinaton of the two nfa's that were on the stack
            #which is what the . means 'Concatenate'
            #push the '.' nfa to the stack
            nfaStack.append(newNFA)
        elif c == '|':
            #doesn't matter what order they are popped of for the or operator
            nfa2= nfaStack.pop()
            nfa1= nfaStack.pop()
            #create two new instances of states
            initial = state()
            accept = state()
            #create a new initial state for both nfa1 and nfa2
            initial.edge1 = nfa1.initial
            initial.edge2 = nfa2.initial
            #create a new accept state for nfa1 and nfa2
            nfa1.accept.edge1 = accept
            nfa2.accept.edge1 = accept
            #just like the drawn out example on paper
            #for the or operator you put a new initial and accept state for whatever nfas you have
            #push the new '|' nfa to the stack
            newNFA = NFA(initial, accept)
            nfaStack.append(newNFA)
        elif c == '*':
            #pop only one nfa off the stack for '*'
            nfa= nfaStack.pop()  
            #create a new initial and accept state
            initial = state()
            accept = state()      
            #connect the intial state two the nfa initial state
            initial.edge1 = nfa.initial
            #connect the new initial state to the new accept state also
            initial.edge2 = accept
            #connect the old accept to the old initial state
            nfa.accept.edge1 = nfa.initial
            #connect the new old accept state to the new accept state
            nfa.accept.edge2 = accept
            #push the new '*' to the stack
            newNFA = NFA(initial, accept)
            nfaStack.append(newNFA)
        #elif c == '+'
        #elif c == '-'
        #elif c == '%'
        else:
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
            newNFA = NFA(initial, accept)
            nfaStack.append(newNFA)

print('WORKS')