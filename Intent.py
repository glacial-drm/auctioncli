
class Intent: # intent implements default actions, with each subclass intent having their own based on states
    def __init__(self):
        self.state = ''
    
    def prompt(): # prompt as in prompt design that uses conversational markers, implemented by each Intent
        pass

class exit(Intent): # example subclass of intent
    def __init__(self):
        super().__init__()
    
    def prompt():
        # match state
            # state = 'angry'
                # rude exit response | consider: auto exit before (like ragequitting)
        pass

class States:
    def __init__(self):
        self.users = [] # list of registered users
        
        # list of states (neutral, )
            # what are states limited to?
            # why call them states and not moods or something
                # sentiments (sentiment analysis)
                    # from nltk.sentiment.vader import SentimentIntensityAnalyzer
        self.states = [] # list of states ()

        self.user_states = {} # dict of user and their current state
        
        self.chatbot_states = [] # limited size list of chatbot states, multi-state interaction
        pass

    