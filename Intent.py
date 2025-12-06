import inspect, sys
from time import sleep
from Search import TXT_Intent, CSV_QA
from Identity import Identity

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

            
    def __init__(self, intent_matcher:TXT_Intent, qa_searcher:CSV_QA, identity:Identity):
        self.intent_matcher = intent_matcher
        self.qa_searcher = qa_searcher
        self.user = identity

        # Intent Managing
        self.intent_list = ['start'] # base case never gets checked as current intent is appended before checking prev intent

        self.partial_prompts = { # include a recoverable yes/no (N-best-lists for intents with multiple branches)
            'exit': 'Did you want to exit?',
            'help': 'Everything ok? Do you need some help?',
            'greeting': '',
            'name-calling': 'Did you want me to fetch your listed name?',
            'question-greeting': 'Were you asking me?',
            'discoverability': 'Did you want to know more?',
            'question-answering': '', # n best lists on questions

            'yes': 'Was that a yes?',
            'no': 'Was that a yes?' # we ask for yes instead of no as the goal is to get their desired intent as input. if they didn't say yes they said no instead
        }

        self.intent_frozen = {
            'state': False,
            'intent': '' 
        }

        # Identity
            # user stats
        self.nickname = 'champ'
        self.greeting = "What's up"
        self.intent_count = {

        }

        # Events
        # load-file
            # FILE SHOULD BE JSON -----------------------------------------------------------------
        self.transaction_list = [('yes', 'buy')] # need an actual base case -----------------------
        # this stuff should go in states
            # list of acknowledgements based on attitude
        
    
    def freeze_intent(self, intent:str, yes_no:bool): # if we want to force a new intent we need to store the intent here
        # why do we want to freeze intent
            # defining methods in terms of each other may lead to recursive definitions which can very easily get out of control when adding scope to project
            # hence refer to a method using the intent key for the method in the outer loop
                # scalable and already part of the infrastructure
        self.intent_frozen['state'] = True
        self.intent_frozen['intent'] = intent

        # Yes/No intent is not appended to intent list, hence we append the passed intent
        if yes_no:  
            self.intent_list.append(intent)
        # we append freeze as the outer loop three_tier confidence call, which typically appends the determined intent, is skipped when the intent is frozen
            # this is possible as we have already determined the intent
        self.intent_list.append('freeze') 
        

    def unfreeze_intent(self):
        self.intent_frozen['state'] = False
        self.intent_frozen['intent'] = ''

    def tutorial(self):
        # match yes, no
            # if not those: you seem to know your stuff
        if self.user.new_user:
            match self.three_tier_input("You seem new. Want me to show you the ropes?"):
                case 'yes': # force special single time outcome for tutorial intent
                    self.freeze_intent(intent='tutorial', yes_no=True)
                    
                case _:
                    pass

    def get_sentiment(self):
        # get sentiment of user input (positive/negative)
            # adjust chatbot mood accordingly
                    # from nltk.sentiment.vader import SentimentIntensityAnalyzer
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
    
    def intent_transaction(self, intent:str):
        # if successful transaction, append to transaction list (don't append to transaction list in three tiered confidence, that only tracks that it is a transaction(?))
        # if(is_transaction):
            # self.transaction_list.append()
        
        # how do we handle undoing ---------------------------------------------------
            # undo, redo : "did you change your mind"
                # two stacks
                    # one for completed actions
                    # one for undone actions
                
            # only append yes and no for transactions
                # transaction flag
        
        if(intent == 'transaction'): # 
            intent = input("What business did you want to do today?")

        match intent:
            case 'buy': # need spellcheck for this + gap filling?, cosine sim?
                # , print current listings in iterable display
                    # search AGAIN LMAO
                        # actually display all the matching listings in some interactive way
                # buying json 
                pass
            case 'sell': # listings
                pass
            case 'bounty':
                pass
            case 'bid':
                pass
            case 'steal': # random chance, gl
                pass
            case 'change-listing': # user can access their listings to change price / remove them
                pass
            case 'secret': # idk
                pass
            case _: # freeze intent in wildcard no?
                pass

        # ask if they want to continue WE BALL, WE ARE ALWAYS IN THE AUCTION HOUSE NOW
            # if so-
            # in retrospect, it's m

    def unexpected_intent(self, expected_intents:list[str]):
        while True:
            match input("Wasn't expecting that, you want to do something else?\nYou: "):
                case yes:
                    pass

    def three_tier_input(self, prompt:str):
        i, s = self.get_new_intent(prompt) # if score greater than 1, skip three tiered
        intent = self.three_tiered_confidence(i, s, False)
        
        return intent

    def three_tiered_confidence(self, intent:str, score:float, is_transaction:bool):
        
        if(score < 0.7): # explicit reprompt
            sleep(1)
            return ''
        elif(score < 0.9): # partial reprompt, matching new intent to help recover
            new_input = input(self.partial_prompts[intent]+"\nYou: ")
            new_intent, new_score = new_input, 0.8 #self.intent_matcher.search_intent(new_input)
            
            new_intent, new_score = self.get_new_intent(self.partial_prompts[intent])
            
            # import random
            # rand = random.randint(0,1)
            # if (rand):
            #     new_score = 1
            #     print("score is 1")
            
            # recursive call to three tiered as we need to verify their confirmation
                # in edge case of their confidence being uncertain (0.7-0.9)
                    # repeat until we get a confirmed intent, then return to original
                        
                        
                        # if intent is something else, 
            new_intent = self.three_tiered_confidence(new_intent, new_score, is_transaction=False) # this is here to get 
            match new_intent: # if intent is yes keep original intent
                case 'yes':
                    pass
                case 'no': # if intent is no return blank intent (back to outer loop)
                    return '' # we don't return a new intent if they say no
                case _:
                    # print("default case")
                    return new_intent
        

        if(is_transaction): # append transaction to this list, recording successful transaction, return intent (could be buy or sell) to original transaction so that can be appended to transaction list
            self.intent_list.append('transaction')
        else:
            if intent not in ["yes", "no"]: self.intent_list.append(intent) # don't append yes and no since there's no branching to be done off an intent of 'yes'

        return intent # third 'invisible' tier using implicit confirmation


    def intent_settings(self):
        # if response not in expected labels
        # match input, but constrain it to yes and no
        match self.three_tier_input(f"We did this one already {self.nickname}, are you sure you want to proceed?"): 
            # make it a while true method and call it back to back based on matched output?
            case 'yes':
                match self.three_tier_input("In that case, I won't ask you next time, is that ok?"):
                    case 'yes':
                        print('Gotcha.') # list of acknowledgements based on attitude
                    case 'no':
                        print('Gotcha.')
            case 'no':
                pass
            case _:
                return   

    def get_prev_intent(self):
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
        
        prev_intent = self.intent_list[len(self.intent_list) - 2] # -2 as by this method the current intent is the last in array (the current intent calls the prev intent method)
        if prev_intent == 'freeze': # we don't want to return frozen as an intent
            prev_intent = self.intent_list[len(self.intent_list) - 3] 

        # list of potential conflicts that lead to other functions
        curr_intent = inspect.stack()[1].function.split('_')[1]
        if(prev_intent == curr_intent):# this should be handled based on intent e.g. if a specific transaction is triggered multiple times. this is the nature of some actions, no?
            print(curr_intent)
            self.intent_settings()

        return prev_intent # return prev if no conflict

    def get_new_intent(self, prompt:str): # wrapper to make getting new intent more traceable
        new_intent, new_score = input(prompt+"\nYou: "), 1 # testing purposes --------------
        # new_intent, new_score = self.intent_matcher.search_intent(input(prompt+"\nYou:"))
        
        return new_intent, new_score
    
    def intent_exit(self):
        # use f string to format response based on chatbot mood ---------------------------
            # state = 'angry'
                # rude exit response | consider: auto exit before (like ragequitting)
        
        # prompt user (possibly)
        match self.get_prev_intent():
            case 'discoverability':
                # print("After all the options, well see you...")
                pass
            case 'question-answering':
                # it was nice/miserable answering your question
                pass
            case 'name-calling':
                # mention name in response from storage
                pass
            case 'exit':
                # print("Awkward silence")
                pass
            case _: # cases: 'question-greeting'
                # print("Goodbye!")
                pass
        
        # perform function
        sys.exit()
    def intent_help(self):
        # match case based on previous method -----------------------------------------------------
            # make help context-based how?
                # previous method doesn't specify that's what they need help with
                    # especially since all states point to each other 
                        # make it based on calling function
                            #  if we match help as a new intent within a function
                                # e.g. transactions

        
        # perform function
        print("Help is on the way!")
        # prompt user (possibly)
        match self.get_prev_intent():
            case 'tutorial':
                print("Welcome to the Tutorial")
            case 'discoverability':
                # 
                pass
            case 'question-answering':
                # 
                pass
            case 'name-calling':
                # 
                pass
            case '':
                # 
                pass
            case _: # cases: 'question-greeting'
                # print("Goodbye!")
                pass
    def intent_greeting(self):
        name=''
        # match case based on previous method ---------------------------------------------
            # check user/chatbot states as well
            # do stuff based on whether we know them, and reputation from csv 
        if(name): 
            print(f"Hello {name}")
        else:
            name = input("Hello, what is your name? ")
            print(f"Nice to meet you {name}")

        # possibly ask if they have anything they want to do, in a conversational way
            # then return their intent
                # use bool to not flag input in outer loop --------------------------------
                    # acting like a directed graph
    def intent_name_calling(self):
        # match case based on previous method ---------------------------------------------
        # hello, what is your name? -> is name in list -> yes - hi name | no - hello new_name
        name='' # placeholder, get name from csv, ---------------------------------------------- 
        if(name): # need to handle intent matching, if name exists in csv -------------------------
            print(f"Hello {name}") # hello, what is your name? -> is name in list -> yes - hi name | no - hello new_name
        else:
            print("You haven't told me your name yet...")
    def intent_question_greeting(self):
        # match case based on previous method ---------------------------------------------
        ip = input("I am fine, how are you? ")
        match ip: # Possibly do some sentiment analysis ------------
            case '':
                print("Not one for small talk I see")
            case _: # use gap filling / sentiment analysis to expand ----------------------
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
    