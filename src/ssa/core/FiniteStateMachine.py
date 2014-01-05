
from TeXableEntity import TeXableEntity

class FiniteStateMachine(TeXableEntity):
    def __init__(self,
                 alphabet      = set(),
                 states        = set(),
                 initial_state = None,
                 accept_states = set(),
                 transitions   = dict()):

        self.accept_states = accept_states
        self.initial_state = initial_state
        self.states        = states
        self.alphabet      = alphabet
        self.transitions   = transitions

    def add_transition(self, source, token, destination):
        """Adds a transition from source to destination on an input
        token.
    
        If such a transition is already defined, a KeyError will be
        raised.
        """
        self.states.add(source)
        self.states.add(destination)
    
        if source not in self.transitions:
            self.transitions[source] = dict()
        elif token in self.transitions[source]:
            raise KeyError('Input token already defined for source.')
    
        self.transitions[source][token] = destination
    
    def set_initial_state(self, state):
        """Set the initial state for this machine.
    
        If the given state is not in the machine's set of states, it will
        be added.
        """
        self.states.add(state)
        self.initial_state = state

    def reset(self):
        self.current_state = self.initial_state
    
    def update(self, token):
        """Updates the state of the machine according to the input token.
    
        If the input token is not defined for the current state, an
        Exception is raised to signal failure.
        """
        if token in self.transition[self.current_state]:
            self.current_state = self.transition[self.current_state][token]
        else:
            raise Exception('The machine has rejected your input')
