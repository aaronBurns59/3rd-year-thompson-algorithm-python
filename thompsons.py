#Aaron Burns
#A program which converts infix notations to postfix notations
def shunt(infix):
    """A function that converts infix notation to postfix notation"""
    #A dictionary allows setting a higher order of precidences for its items
    #dictionaries are order by strings precidence not an index like an array
    specials= {'*':50, '+':49, '.': 40, '|': 30}

    #return after the infix has been changed to postfix
    postfix=''
    #push and pop operators to this string (push from infix - pop to postfix)
    stack=''

    for c in infix:
        if c == '(':
            stack = stack + c
        elif c == ')':
            #[-1] means the last element in the stack
            while stack[-1] != '(':
                postfix, stack = postfix + stack[-1], stack[:-1]
                #sets the stack equal to upto the last character but not including
                #removes last character from stack
            #run again to delete the closing bracket
            stack= stack[:-1]
        #if the character in the dictionary
        elif c in specials:
        #once you've read a special character
            while stack and specials.get(c, 0) <= specials.get(stack[-1],0):
                postfix, stack = postfix + stack[-1], stack[:-1]
            #puts the special character on the stack
            stack = stack + c
        else:
            postfix = postfix + c
        #anything thats at the end of the stack is added to the postfix and removed from the stack
    while stack:
        #postfix = postfix + stack[-1]
        #stack= stack[:-1]
        #can do all in one line
        postfix, stack = postfix + stack[-1], stack[:-1]
    return postfix

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
    #NB!!! must have 2 underscores at each side for constructor to take in args properly
    def __init__(self, initial, accept):
        #self.initial/accept is the class var after = is the local var
        self.initial=initial
        self.accept=accept

#populate using the result of the shunting yard algroithm
def compile(postfix):
    """A function which creates NFA's from the postfix expressions created by the shunt function"""
    nfaStack = []
    #for creating an nfa fragment for a non special character
    for c in postfix:
        if c == '.':
            #stacks are LIFO pop the last one off the stack first
            nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
            #combine the two states together
            nfa1.accept.edge1 = nfa2.initial
            #push a new nfa onto the stack that is a combinaton of the two nfa's that were on the stack
            #which is what the . means 'Concatenate'
            #push the '.' nfa to the stack
            newNFA = NFA(nfa1.initial, nfa2.accept)
            nfaStack.append(newNFA)
        elif c == '|':
            #doesn't matter what order they are popped of for the or operator
            nfa2, nfa1 = nfaStack.pop(), nfaStack.pop()
            #create two new instances of states
            initial, accept = state(), state()
            #create a new initial state for both nfa1 and nfa2
            initial.edge1, initial.edge2 = nfa1.initial, nfa2.initial
            #create a new accept state for nfa1 and nfa2
            nfa1.accept.edge1, nfa2.accept.edge1 = accept, accept
            #just like the drawn out example on paper
            #for the or operator you put a new initial and accept state for whatever nfas you have
            #push the new '|' nfa to the stack
            newNFA = NFA(initial, accept)
            nfaStack.append(newNFA)
        elif c == '*':
            #pop only one nfa off the stack for '*'
            nfa= nfaStack.pop()  
            #create a new initial and accept state
            initial, accept = state(), state()   
            #connect the intial state two the nfa initial state
            #connect the new initial state to the new accept state also
            initial.edge1, initial.edge2 = nfa.initial, accept
            #connect the old accept to the old initial state
            #connect the new old accept state to the new accept state
            nfa.accept.edge1, nfa.accept.edge2 = nfa.initial, accept
            #push the new '*' to the stack
            newNFA = NFA(initial, accept)
            nfaStack.append(newNFA)
        #elif c == '+'
        #elif c == '-'
        #elif c == '%'
        else:
            #creating a new instance of the state class
            accept, initial = state(), state()
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
    return nfaStack.pop()

def followes(state):
    """Return the set of states that can be reached from state following edge arrows"""
    #create a new set with state as it only member
    states = set()
    states.add(state)
    #Checks if the state has arrows labled e from it
    if state.label is None:
        #check if edge1 is a state
        if state.edge1 is not None:
        #if there is an edge1 follow it
        #union operator = |
            states |= followes(state.edge1)
        #check if edge2 is a state
        if state.edge2 is not None:
            #if there is an edge2 follow it
            states |= followes(state.edge2)
        #the only time there isn't an edge1 if for the accept state
    return states

def match(infix, string):
    """Matches the string to the infix regular expression"""
    #Shunt and compile the regular expression 
    postfix = shunt(infix)
    nfa = compile(postfix)
    #The current set of states only one copy of an item allowed in a set
    currentSet = set()
    #The next set of states
    nextSet = set()

    #Add the initial state to the current set
    currentSet |= followes(nfa.initial)

    #loop through each character in the string 
    for s in string:
        #loop through the current set of states
        for c in currentSet:
            #check if that state is labelled 'x'
            if c.label == s:
                #add the edge1 state to the next set including all the states you can get to by following e arrows
                nextSet |= followes(c.edge1)
            # set the current state to next
        currentSet = nextSet
        # clear the next state
        nextSet = set()
        # checks if the accept state is in the current set of state
    return (nfa.accept in currentSet)

# TESTS
#tuple used to store test data
test = [
    ('a.b.c', ''),
    ('a.(b|d).c', 'abc')
]

for exp, res in test:
    print(match(exp, res), exp, res)
#infixes = ['a.b.c', 'a.(b|d).c', '(a.(b|d))', 'a.(b.b)*.c']
#strings = ['', 'abc', 'abbc', 'abcc', 'abad', 'abbbc']
#
#for expression, expected_output in zip(infixes, strings):
#    print(match(expression, expected_output), expression, expected_output)

#for i in infixes:
#    for s in strings:
#        print(match(i,s), i, s)

