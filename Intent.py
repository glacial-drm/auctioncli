import inspect, sys
from Search import TXT_Intent, CSV_QA

class IntentManager: # intent implements default actions, with each subclass intent having their own based on states
    def __init__(self):
        pass

class Intent:
    # lessons learnt
        # can't define classes/methods in terms of each other because recursion
            # hence each reference has to be independent and cannot point to another reference
                # unless that reference doesn't point to another reference
        # don't overcomplicate
            # goal was originally to create architecture similar to a directed graph
            # we can imply this using match case and checking previous intent
            # we can also constrain the response by passing labels to the search item
    # new goal
        # use 'inspect.stack()[2].code_context' to track the previously called method, acting as a graph without the necessary infrastructure
        # restrict the scope of methods that call other methods
            # this is only necessary for methods that have sub-calls
                # transaction
                    # loop for these methods (cases linked to each other)
                        # generic case catches any of the non-loop methods -> break
                    # SMALL TALK SHOULD BE PART OF TRANSACTION, one loop --------------------------

            
    def __init__(self, intent_searcher:TXT_Intent, qa_searcher:CSV_QA):
        self.search_intent = intent_searcher
        self.search_qa = qa_searcher
        self.intent_list = ['start1']
        
        # this stuff should go in states
        self.nick = 'champ'
        # load-file
        self.intent_count = {

        }
    
    def start(self):

        pass
    
    def gap_filling(self, keyword:str, user_input:str):
        # if keyword found in input return true
            # combine with three tiered ig
            # warning
            # 
        pass
    
    def write_file(self):
        # write to file
        # save file
        pass

    def unexpected_intent(self, expected_intents:list[str]):
        while True:
            match input("Wasn't expecting that, you want to do something else?\nYou: "):
                case yes:
                    pass
    
    def intent_settings(self):
        i = input(f"We did this one already {self.nick}, are you sure you want to proceed?\nText goes here:")
        # if response not in expected labels
        # match input, but constrain it to yes and no
        match i: # can't do match_yes_no method as it would be recursive and passed labels would need to change
            case 'yes':
                j = input("In that case, I won't ask you next time, is that ok?")
                match j:
                    case 'yes':
                        print('Gotcha.')

    def get_prev_intent(self, curr_intent:str):
        # Backwards step until we find a key within our defined methods
            # queue
                # we need a base case (within our desired keys)
                # length of list-1
            # for things that check total number of interactions (based on current user)
                # store in file each call, prevents the need to 
            # --------------------------
            # What if we want to have memory greater than 1, what for?
                # transaction: not for checking previously bought items 
                    # we would rather keep track of user stats to determine output
                        # if successful transactions > 3 then valued customer etc
                # discoverability, exit, help, 
                    # literally no reason       
        prev_intent = self.intent_list[len(self.intent_list) - 1]
        if(prev_intent == curr_intent):# this should be handled based on intent e.g. if a specific transaction is triggered multiple times. this is the nature of some actions, no?
            self.intent_settings()

        return 
        
    def intent_exit(self):
        # match case based on the previous method -------------------------------------------------
            # hence having generic case
        # UNDER NO CIRCUMSTANCE CAN WE CALL ANOTHER METHOD ----------------------------------------
        
        self.get_prev_intent()
        # perform appropriate function
        # match state
            # state = 'angry'
                # rude exit response | consider: auto exit before (like ragequitting)

        print("Goodbye!")
        sys.exit()
        
    def intent_help(self):
        # match case based on previous method -----------------------------------------------------

        print("Help is on the way!")

    def intent_greeting(self):
        name=''
        # match case based on previous method -----------------------------------------------------
            # check user/chatbot states as well
            # do stuff based on whether we know them, and reputation from csv 
        if(name): 
            print(f"Hello {name}")
        else:
            name = input("Hello, what is your name? ")
            print(f"Nice to meet you {name}")

    def intent_name_calling(self):
        # match case based on previous method -----------------------------------------------------
        # hello, what is your name? -> is name in list -> yes - hi name | no - hello new_name
        name='' # placeholder, get name from csv, ---------------------------------------------- 
        if(name): # need to handle intent matching, if name exists in csv -------------------------
            print(f"Hello {name}") # hello, what is your name? -> is name in list -> yes - hi name | no - hello new_name
        else:
            print("You haven't told me your name yet...")

    def intent_question_greeting(self):
        # match case based on previous method -----------------------------------------------------
        ip = input("I am fine, how are you? ")
        match ip: # Possibly do some sentiment analysis ------------
            case '':
                print("Not one for small talk I see")
            case _:
                print("That's nice, or maybe it isn't...")

    def intent_discoverability(self):
        # match case based on previous method -----------------------------------------------------
            # specify auction functions when prev is to do with auction, and so on for any nested ones
        print("I can meet all the criteria for the checkpoint and more:)")

    def intent_qa(self, question:str):
        # match case based on previous method -----------------------------------------------------
        answers = self.search_qa.search_qa(query=question)
        
        if(answers):
            for ans in answers:
                print(ans)   

    def prompt_intent(self, intent:str): 
        """Call the prompt() function of the provided intent key, changing the current intent"""
        
        self.intents[intent].prompt()

    
class help_inten(Intent): # example subclass of intent
    def __init__(self):
        # super().__init__()
        pass

    def prompt(self): # Get calling(?) intent to make help context-based
        # each other intent would be hardcoded, they're all simple anyway
            # make this the default case where all generic functions are 
        # transaction
            # default
                # welcome to the auction house...
            # buy
                # you can buy stuff
            # etc
        print("Help is on the way! (adding help command closer to completion)")

        # then match new intent
            # directed graph 
            # restrict intents in some way in some cases????
        
        # self.intents(self.get_new_intent()).prompt()
        self.prompt_intent(intent="greeting")
        

class transaction(Intent):
    def __init__(self):
        pass
    def prompt(self):
        pass

class States:
    def __init__(self):
        self.users = [] # list of registered users
        
        # list of states (neutral, )
            # what are states limited to?
            # why call them states and not moods or something
                # sentiments (sentiment analysis)
                    # from nltk.sentiment.vader import SentimentIntensityAnalyzer
        self.states = ['happy', 'sad'] # list of states ()

        self.user_states = {
            'happy': 0.1,
            'sad': 0.0

        } # dict of user and their current state, export possibly to keep track ----------------------------------------------
        
        self.chatbot_states = {

        } # limited size list of chatbot states, multi-state interaction | do we keep it consistent or based on user, consistent is cool because of npc -------------------------
        pass

    