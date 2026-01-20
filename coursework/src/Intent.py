import inspect, sys
from time import sleep

from nltk.corpus import words, wordnet as wn
from nltk.util import ngrams
from nltk.metrics.distance import jaccard_distance

from joblib import load

from Search import TXT_Intent, CSV_QA
from Identity import IdentityManager
from Transaction import TransactionManger



class IntentManager:
    def __init__(self, intent_matcher:TXT_Intent, qa_searcher:CSV_QA, identity:IdentityManager, transaction: TransactionManger):
        # Constructor Parameters
        self.intentMatcher = intent_matcher
        self.qaSearcher = qa_searcher
        self.users = identity
        self.items = transaction

        # Intent Managing

        # Base case for intent tracking needed as prev intent is len(intent_history) - 2
            # this is as current intent, method calling get_prev_intent is appended to end of list
        self.intentHistory = ['start']

        self.intents = ['exit', 'help', 'greeting', 'name-calling', 'question-greeting', 'discoverability', 'question-answering', 'freeze', 'unfreeze']
        self.transactionIntents = ['buy', 'sell', 'bounty', 'bid', 'transaction', 'search', 'steal'] #'purchase' used to be in here but that doesn't map

        self.partialPrompts = {
            'exit': 'Did you want to exit?',
            'help': 'Everything ok? Do you need some help?',
            'greeting': '',
            'name-calling': 'Did you want me to fetch your listed name?',
            'question-greeting': 'Were you asking me?',
            'discoverability': 'Did you want to know more?',
            'question-answering': '', # n best lists on questions
            'transaction': 'Did you want to make a transaction?',
            'yes': 'Was that a yes?',
            'no': 'Was that a yes?' # we ask for yes instead of no as the goal is to get their desired intent as input. if they didn't say yes they said no instead
        }
        self.repeatPrompts = { 
            # only for (most) transactions
                # small talk intents (above) are easily repeatable.
                # (most) transactions have depth, making it annoying to have to re-type
            'buy': 'buy',
            'sell': 'sell',
            'bid': 'bid on',
            # 'bounties' # not for bounties for the same reason as small talk
            'steal': 'steal',
            'search': 'search for'
        }

        self.intentFrozen = {
            'state': False,
            'intent': '' 
        }

        self.duplicateNotice = True
        self.otherNotices = True

    def split_output(self, str1:str, str2:str):
        '''This method allows for differing output prompts based on the system's perception of the user'''
        if self.users.jsonUsers[self.users.currentUser]['system-mood'] > 0.5:
            self.staggered_output(str1)
        else:
            self.staggered_output(str2)

    def split_input(self, str1:str, str2:str):
        '''This method allows for differing input prompts based on the system's perception of the user'''
        if self.users.jsonUsers[self.users.currentUser]['system-mood'] > 0.5:
            input(str1+"\nYou:  ")
        else:
            input(str2+"\nYou:  ")
    def disambiguation(self, user_input:str):
        '''This method prevents and as a keyword, disambiguating instances of too much information'''
        if user_input == None or user_input == "":
            return user_input
        
        x = user_input
        if 'and' in user_input:
            print(user_input.split("and",1))
            x = input("Could you specify the more important query please?:\nYou:  ")
        
        return x    
    def sentiment_mood(self, user_input:str):
        '''This method uses sentiment analysis to punish or benefit the user based on their input'''
        # get sentiment of user input (positive/negative)
            # adjust system mood accordingly

        if user_input == None or user_input == "":
            return

        
        vect = load('./resources/models/vectorizer.joblib')
        transf = load('./resources/models/transformer.joblib')
        clf = load('./resources/models/classifier.joblib')

        processed_newdata = vect.transform([user_input])
        processed_newdata = transf.transform(processed_newdata)


        curr_user_system_mood =  self.users.jsonUsers[self.users.currentUser]['system-mood']
        match clf.predict(processed_newdata)[0]:
            case 'positive':
                
                if curr_user_system_mood < 1:
                    self.users.jsonUsers[self.users.currentUser]['system-mood'] += 0.1
            case 'negative':
                if curr_user_system_mood > 0:
                    self.users.jsonUsers[self.users.currentUser]['system-mood'] -= 0.1
        
        self.users.write_json()
    def spellcheck(self, _input:str):
        '''This method uses nltk.wordnet to check the spelling of user input'''
        list_words = _input.split(' ')
        list_correct_words = []
        correct_words = words.words()
        
        try:
        # REFERENCE: geeksforgeeks | https://tinyurl.com/4b7x92ys ====================
            for word in list_words:
                temp = [(jaccard_distance(set(ngrams(word, 2)),
                                        set(ngrams(w, 2))),w)
                        for w in correct_words if w[0]==word[0]]
                list_correct_words.append(sorted(temp, key = lambda val:val[0])[0][1])
        # ============================================================================
        except:
            pass
        else: 
            correct_words = ' '.join(str(x) for x in list_correct_words)
            # print(list_correct_words)
            intent = self.three_tiered_input(f"Did you mean {correct_words}?")
            match intent:
                case 'yes':
                    return correct_words
                case 'no':
                    intent_2 = self.three_tiered_input(f"Do you want to keep your initial input?")
                    match intent_2:
                        case 'yes':
                            return _input
                        case 'no':
                            return self.spellcheck(input("What did you mean to say?\nYou:  "))      
                        case _:
                            if intent in self.intents or self.transactionIntents:
                                self.freeze_intent(intent=intent_2, append=False)
                case _:
                    if intent in self.intents or self.transactionIntents:
                        self.freeze_intent(intent=intent, append=False)
    
    def synres_three_tier(self, prompt:str):
        '''Method that uses the pattern in main to combine both intent matching methods'''
        x = self.three_tiered_input(prompt)
        
        if x != "":
            
            return x
        
        for keyword in self.transactionIntents: # three tiered is more specific to small talk | synoynm resolution allows for transaction intents to be matched with nltk data
            sub_intent = self.synonym_resolution(keyword, prompt)
            if keyword != sub_intent: continue
            if sub_intent != None: # if synonym resolution matches, force the transaction intent
                print(sub_intent)
                return sub_intent
        
        return prompt
                    

    def synonym_resolution(self, keyword:str, user_input:str): # previously referred to as gap filling
        '''This method generates synonyms and derivative formms, attempting to intent-match the user's input using them'''
        # if keyword synonym found in input return keyword
            # get synonyms and match
                # synonym resolution (homonym resolution is disambiguation)
            # get different forms of words as well
        if user_input == None: return

        synonyms = []
        exceptions = ['call', 'steal']
        #print(keyword)
        for synset in wn.synsets(keyword):
            for lemma in synset.lemmas():
                
                synonym = lemma.name()
                if synonym not in synonyms: synonyms.append(synonym)
                
                related = lemma.derivationally_related_forms()
                for r in related:
                    if r.name() not in synonyms: synonyms.append(r.name())
                
                if 'call' in synonyms: # case to remove words
                    synonyms.remove('call') # maps name calling to bid
                    synonym = ''
                    continue
                elif 'steal' in synonyms and keyword == 'buy': # case to remove words
                    synonyms.remove('steal') # maps name calling to bid
                    synonym = ''
                    continue

                if synonym in user_input:
                    # print(synonym)
                    return keyword
        
        # print(synonyms)

    def append_intent(self, intent:str):
        '''This is a wrapper method to make intent appends to history more traceable'''
        # This method filters out wildcard intents and yes/no
            # wildcard intents don't exist to the system, we use cosine sim / synonym resolution to map to a given intent
            # don't append yes and no since there's no branching to be done off an intent of 'yes'

        if intent in self.intents or intent in self.transactionIntents: 
            # print("appending: "+intent)
            # print(inspect.stack()[1].function)
            self.intentHistory.append(intent)
    def repeat_intent(self, repeating_intent:str): # may need is_transaction if we do undo/redo
        '''This enables the user to repeat the previous intent'''
        self.users.write_json()
        self.items.write_json()

        intent = self.three_tiered_input(f"Do you want to {self.repeatPrompts[repeating_intent]} another item?")
        
        match intent:
            case 'yes':
                # Contrary to other freezes, append is True here as the intent matched was not the desired intent
                    # We repeat the old intent in this case, as opposed to the new one matched by three_tier_input
                        # Don't worry, yes and no are not appended to history in three_tiered_input
                self.freeze_intent(intent=repeating_intent, append=True)
            case 'no':
                self.unfreeze_intent()
            case _:
                if intent in self.intents or self.transactionIntents:
                    self.freeze_intent(intent=intent, append=False)
    def freeze_intent(self, intent:str, append:bool): # if we want to force a new intent we need to store the intent here
        '''This method freezes the intent of the next iteration if one is passed in the current iteration
        This mimics the function of an interconnected graph, with most nodes having connecting edges'''
        # why do we want to freeze intent
            # defining methods in terms of each other may lead to recursive definitions which can very easily get out of control when adding scope to project
            # hence refer to a method using the intent key for the method in the outer loop
                # scalable and already part of the infrastructure
        self.intentFrozen['state'] = True
        self.intentFrozen['intent'] = intent

        # Not all match case statements append the intent of the user to history when matching
            # Why?
                # Not every step is for intent, e.g. naming an item in a transaction
            # If three_tiered_input has been called within the intent, append = False as we don't want to append the intent to history again.
                # append = False
                # yes and no are recognised intents that are not appended regardless
            # If three_tiered_input hasn't been called, then we need to append the new intent
                # append = True
        if append:  
            self.append_intent(intent)
        
        # freeze is detected at start of I/O loop and removed at end
            # this is possible as we have already determined the intent
        self.append_intent('freeze') 
    def unfreeze_intent(self):
        '''This method unfreezes the current intent'''
        self.intentFrozen['state'] = False
        self.intentFrozen['intent'] = ''
    
    def three_tiered_input(self, prompt:str):
        '''This method combines three-tiered confidence with user input as a wrapper method'''
        # Called each iteration in loop
        # for intent in self.transactionIntents:
        #     if intent in prompt:
        #         return intent
        
        i, s = self.get_new_intent(prompt) # if score greater than 1, skip three tiered
        intent = self.three_tiered_confidence(i, s, False)
        
        return intent
    def get_new_intent(self, prompt:str): # wrapper to make getting new intent more traceabl
        '''This method is a wrapper for using the Intent Match object to get a new user input Intent'''
        # new_intent, new_score = input(prompt+"\nYou:  "), 1 # testing purposes --------------
        new_intent, new_score = self.intentMatcher.search_intent(input(prompt+"\nYou: "))
        
        return new_intent, new_score
    def three_tiered_confidence(self, intent:str, score:float, is_transaction:bool):
        '''This method uses multiple different confirmation techniques based on the cosine similarity output the user prompt'''
        if(score < 0.7): # explicit reprompt
            sleep(1)
            return ''
        elif(score < 0.9): # partial reprompt, matching new intent to help recover
            #new_input = input(self.partialPrompts[intent]+"\nYou:  ")
            # new_intent, new_score = new_input, 1 #self.intentMatcher.search_intent(new_input)
            new_intent, new_score = self.get_new_intent(self.partialPrompts[intent])
            # import random
            # rand = random.randint(0,1)
            # if (rand):
            #     new_score = 1
            #     print("score is 1")
            
            # recursive call to three tiered as we need to verify their confirmation
                # in edge case of their confidence being uncertain (0.7-0.9)
                    # repeat until we get a confirmed intent, then return to original
                        # intent is yes passes to return original intent
                        # intent is no returns nothing, so we exit method back to loop
                        # if intent is something else, return the new intent
            new_intent = self.three_tiered_confidence(new_intent, new_score, is_transaction=False) # this is here to get 
            match new_intent: # if intent is yes keep original intent
                case 'yes':
                    pass
                case 'no': # if intent is no return blank intent (back to outer loop)
                    return '' # we don't return a new intent if they say no
                case _:
                    # print("default case")
                    return new_intent
        
        # ideally we don't append transaction intents here as they aren't guaranteed to be completed correctly
            # fix issue by getting intens to return a success indicator, then: --------------------
        # if intent not in self.intents:
        # also an issue with intent being appended despite not being in the corresponding intent method  --------------------------------------------------------------------------------
        self.append_intent(intent)

        return intent # third 'invisible' tier using implicit confirmation


    def intent_settings(self):
        '''This method allows for some notices to be disabled'''
        if self.duplicateNotice:
            intent = self.three_tiered_input(f"We did this one already {self.users.currentUser}, are you sure you want to proceed?")
            match intent:
                case 'yes':
                    match self.three_tiered_input("In that case, I won't ask you next time, is that ok?"):
                        case 'yes':
                            print('Gotcha.') # list of acknowledgements based on attitude
                            self.duplicateNotice = False
                        case 'no':
                            print('Gotcha.')
                        case _:
                            if intent in self.intents or intent in self.transactionIntents:
                                self.freeze_intent(intent, append=False) 
                            
                            return # return called here as there are other match-cases that can potentially mess with freezing
                case 'no':
                    pass
                case _:
                    if intent in self.intents or intent in self.transactionIntents:
                        self.freeze_intent(intent, append=False) 
                    
                    return # same as above default case

        if self.otherNotices:
            intent_2 = self.three_tiered_input(f"Do you want notices to remain on?")
            match intent_2:
                case 'yes':
                    pass
                case 'no':
                    self.otherNotices= False
                case _:
                    if intent in self.intents or intent in self.transactionIntents:
                        self.freeze_intent(intent, append=False) 

    def staggered_output(self, output:str):
        '''This method forces the user to press enter to continue'''
        print(output+" | (Enter)") 
        
        while True:
            if input("") == "":
                break
    
    def get_prev_intent(self):
        '''This method returns the calling method from stack memory'''
        
        # for things that check total number of interactions (based on current user)
        # we would ideally rather keep track of user stats to determine output
            # if successful transactions > 3 then valued customer etc     
        # print(self.intentHistory)
        prev_intent = self.intentHistory[len(self.intentHistory) - 2] # -2 as by this method the current intent is the last in array (the current intent calls the prev intent method)

        
        # print("awoo: "+inspect.stack()[1].function) # get calling function 
        curr_intent = inspect.stack()[1].function.split('_')[1] # calling functions can only be in format 'intent_x' (hence the '_' delimiter)
        if(prev_intent == curr_intent):# this should be handled based on intent e.g. if a specific transaction is triggered multiple times. this is the nature of some actions, no?
            # print("AGAIN: "+curr_intent)
            prev_intent = self.intent_settings()


        if prev_intent == 'freeze': # we don't want to return frozen as an intent | we may want to now
            pass
            # prev_intent = self.intentHistory[len(self.intentHistory) - 3] 
        

        return prev_intent # return prev if no conflict


    def intent_tutorial(self):
        '''This is the dialog tree for the tutorial'''
        if self.users.newUser:
            self.append_intent('tutorial')
            match self.three_tiered_input("You seem new. Want me to show you the ropes?"):
                case 'yes':
                    self.intent_help()
                    # self.freeze_intent(intent='tutorial', append=True)  # this maps to the help method, combining any help text as a tutorial
                    # self.intentHistory.append('unfreeze') # unfreeze so 
                case 'no':
                    pass

    def intent_exit(self):
        '''This is the dialog tree for the exit intent'''
        
        # prompt user (possibly)
        match self.get_prev_intent():
            case 'discoverability':
                print("After all those options... Well see you...")
            case 'question-answering':
                # print(f"It was {nice/miserable} answering your question, goodbye")
                pass
            case 'name-calling' | 'greeting':
                # print(f"{Pleasure/disdainful} doing business with you {nickname/self.users.currentUser}.")
                    # switch between nickname/name based on greatest chatbot mood
                pass
            case _: # known cases: 'question-greeting' |
                # print("Goodbye!")
                pass
        
        # perform function
        sys.exit()
    
    def intent_help(self):
        '''This is the dialog tree for the help method'''
        # if current user is a criminal then we deny help --------------------------------------
            # return      
        
        # transaction intents fail to be fetched here, last day bug...
            # issue is that three_tiered_input only predicts on small talk intents (excluding transactions)
                # this was after reimplementing the intent classifier built earlier, which lacked data for transactionala intents
                # definitely fixable, just lack the time, sorry :(
        intent = self.three_tiered_input("Welcome to the Help Desk\nWhat would you like to learn more about?\n"+str(self.intents)+"\n"+str(self.transactionIntents))
        
        # intent = self.synres_three_tier(prompt= "Welcome to the Help Desk\nWhat would you like to learn more about?\n"+str(self.intents)+"\n"+str(self.transactionIntents))
        match intent: # three tier input needs synonym_resolution in some way to match intents
            case 'discoverability':
                self.staggered_output("Discoverability allows you to get all the deets about the Auction House straight. Make sure to go there if you want an overall summary!")
            case 'name-calling':
                self.split_output("According to some people, going to the front desk can switch you into a different person...","I think you should go to the front desk, get a new name or something.")
                self.split_output("Crazy right?","Yea, no point in still talking to you")
            case 'question-greeting' | 'greeting':
                self.staggered_output("You can get to know the front desk this way, pretty neat huh?")
            case 'question-answering':
                self.staggered_output("Try asking the front desk that question.")
            case 'exit':
                self.staggered_output("If you ever want to leave, just leave through the front (desk)!")
                self.staggered_output("On a more serious note, you should be able to leave at any given time...")
                self.staggered_output("Just try not to be in the middle of a transaction when doing so that doesn't usually end well...")
            case 'help':
                self.staggered_output(". . .")
                self.staggered_output("You're alread in the right place!")
            case 'buy':
                self.staggered_output("Buying is the process of exchanging money for items listed in the auction house...")
                self.staggered_output("You can access the buying menu by requesting to buy at the front desk!")
            case 'sell':
                self.staggered_output("Selling allows you to list an item of your choice on the marketplace...")
                self.staggered_output("It would be nice if someone bought it, though that can take some time...")
                self.staggered_output("To get to the selling menu, try asking about it at the front desk!")
            case 'bounty':
                self.staggered_output("Bounties are put on known criminals, offering a cash prize for their capture...")
                self.staggered_output("To see the current bounties, try mentioning it at the front desk")
                pass
            case 'bid':
                self.staggered_output("Bidding allows you to place your interest in an item on the market...")
                self.staggered_output("Not all items can be bid on though, this distinction is at the sellers discretion...")
                self.staggered_output("If you want to bid, try asking the front desk.")
            case 'transaction':
                self.staggered_output("Transaction is the umbrella term that contains actions to do with items, money and users within the Auction House...")
                self.staggered_output("These actions include: buying, selling, bounty-viewing...")
                self.staggered_output("bidding, changing (item listings) and searching (for items).")
                self.staggered_output("To reach the Transaction Menu, try requesting a transaction at the front desk!")
            case 'change':
                self.staggered_output("To change one of the items you have listed when selling, try asking the front desk to change an item.")
            case 'search':
                self.staggered_output("You can make use of a search feature to find a specific item currently listed on the shop...")
                self.staggered_output("The details of this item will be presented to you if it is found...")
                self.staggered_output("This can be reached from the front desk")
            case 'steal':
                self.staggered_output("It's a free land, you can always try...")
                self.staggered_output("...just don't complain when it comes back to bite you")
            # case 'secret' # shouldn't be a case for secret
            case '':
                pass
            case _:
                # freeze not needed, all intents covered here
                # self.freeze_intent(intent, append=True)
                pass
        
        # question answering does not map to outputting an answer here
            # limit using notices ----------------------------------------
        if not self.duplicateNotice:
            self.staggered_output("Try asking a question sometime, you never know what might happen!")

        # repeat intent
            # keep or change the match text

    def intent_greeting(self):
        '''This is the dialog tree for the greeting intent'''
        name = self.users.currentUser
        
        # check user/chatbot states as well ------------------------------------------------------
            # do stuff based on whether we know them, and reputation from json
        if(name): 
            print(f"Hello {name}")
        # possibly ask if they have anything they want to do, in a conversational way
            # then return their intent
                # use bool to not flag input in outer loop --------------------------------
                    # acting like a directed graph
    def intent_name_calling(self):
        # match case based on previous method ---------------------------------------------
        # hello, what is your name? -> is name in list -> yes - hi name | no - hello new_name   

        name = self.users.currentUser
        self.split_output(f"Hello {name}...","...")
        intent = self.three_tiered_input(f".....are you {name}?")
        match intent:
            case 'yes':
                self.staggered_output("Ok...")
            case 'no':
                self.users.load_user(input("What is your name? New or old it matters not.\nYou:  ")) # make \nYou:  formatted input function, then use that and pass it into three tiered whenever needed
                # verify changing active user works ----------------------------------------------------------------
                return
            case _:
                if intent in self.transactionIntents or intent in self.intents:
                    self.freeze_intent(intent, False) 
                    return
        
        
        # change nickname --------------------------------------
        self.split_output(f"How about your nickname...","... and your nickname...")
        intent_2 = self.split_input(f".....do you like being called {self.users.jsonUsers[name]['nickname']}?", f"...can you tolerate being called {self.users.jsonUsers[name]['nickname']}?")
        
        match intent_2:
            case 'yes':
                self.staggered_output("OK...")
                self.staggered_output("run along now...")
            case 'no':
                self.users.jsonUsers[name]['nickname'] = input("What is your nickname? Un-nicknamed one..\nYou:  ")
                self.users.write_json() # THIS REALLY SHOULDN'T BE HERE BUT THIS METHOD IS ONLY USED HERE SO IT'S FINE FOR NOW
            case _:
                if intent in self.transactionIntents or intent in self.intents:
                    self.freeze_intent(intent, False) 

            
    def intent_question_greeting(self):
        '''This is the dialog tree for the question-greeting intent, such as how are you?'''
        
        # match case based on previous method ---------------------------------------------
        intent = input("I am fine, how are you? ")
        match intent: # Possibly do some sentiment analysis ------------------------------------------
            case '':
                print("Not one for small talk I see")
            case 'positive':
                print("That's nice, or maybe it isn't...")
            case 'negative':
                print("That's not nice, or maybe it is...")
            case _: # wildcard freeze (maybe not because sentiment analysis)
                if intent in self.transactionIntents or intent in self.intents:
                    print(intent)
                    self.freeze_intent(intent, True)
                
    def intent_discoverability(self): # conversational markers -----
        '''This is the dialog tree for the discoverability intent'''

        self.staggered_output("Welcome to the Auction House Discoverability Summary...")
        self.staggered_output("The House is split into two main sections...")
        self.staggered_output("The Front desk and the Transaction desk...")
        self.staggered_output("The Front desk is suitable for all your needs, and is the main point of contact for most actions...")
        self.staggered_output("Here just state your action and it will 100%, rest assured be carried out as intended...")
        self.staggered_output("(We have the right to reserve judgement on the accuracy of this claim, that's for the evaluation)...")
        self.staggered_output("The Transaction desk is more specific to buying and selling on the market, among other functions...")
        self.staggered_output("If you need help with something specific, don't hesitate to say so at the front desk!")

    def intent_qa(self, question:str):
        '''This is the where question answering is handled, returning an appropriate answer'''
        answers = self.qaSearcher.search_qa(query=question)
        
        if(answers):
            for ans in answers:
                print(ans)      
        else:
            print("Your question doesn't have an answer")
    
    def intent_transaction(self, intent:str):
        '''This is where the transaction intents are routed. Each is directed to a different method'''
        # how do we handle undoing ----------------------------------------------------------------
            # undo, redo : "did you change your mind"
                # two stacks
                    # one for completed actions
                    # one for undone actions
                # this only applies to transaction methods
                    # search using x in self.transactionIntents

        # if user.status != criminal and user.transaction_total > num (transaction total) ---------
            # welcome valued customer
        # and the opposite

        if(intent == 'transaction' or intent == 'auction'): # 
            intent = input("What business did you want to do today?\nYou:  ")

        match intent:
            case 'buy': # need spellcheck for this
                # print current listings in iterable display -------------------------------------
                    # actually display all the matching listings in some interactive way
                self.items.buy()
                self.repeat_intent(intent) # may need is_transaction if we do undo/redo
            case 'sell':
                partial_item = self.items.sell() # item is partial as we use three tiered input to get yes/no
                
                if partial_item == {}:
                    self.repeat_intent(intent)
                    return

                match self.three_tiered_input((f"Should {partial_item['title']} be put up for auction?:")):
                    case 'yes':
                        self.items.create_item(self.users.currentUser, partial_item['title'], partial_item['price'], partial_item['count'], bidding=True)
                    case 'no':
                        self.items.create_item(self.users.currentUser, partial_item['title'], partial_item['price'], partial_item['count'], bidding=False)
            case 'bid':
                self.items.bid()
                self.repeat_intent(intent)
            case 'bounty':
                self.items.bounty()
                self.staggered_output(f"Keep an eye out for those thugs...")
                self.staggered_output("...and make not to accuse strangers.")
            # case 'change-listing': # user can access their listings to change price / remove them
            #     self.items.change_listing()
            #     self.repeat_intent(intent)
            case 'search':
                self.items.search_item(input("Which item are you looking for?: "))
            case 'steal':
                self.items.steal()
                self.repeat_intent(intent)
            case 'secret':
                self.items.secret()
            case _:
                self.freeze_intent(intent, True)
        
        # update user status after successful transaction
            # create function for below
            # if (some function on chatbot state) < x
                # change status to x
        
        # append prev intents? (independent of three tier)
            #