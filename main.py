from time import sleep
import Search, Intent, Identity, Transaction, Event
import nltk
import warnings
def main():

    warnings.filterwarnings('ignore')  # some warnings were caused by single token input, program still runs good though.
    nltk.download('all') # hoping this is already done in the assessment

    QA = Search.CSV_QA(path='./resources/model_data/COMP3074-CW1-Dataset_500.csv')
    intentMatch = Search.TXT_Intent(folder_path='./resources/model_data/intent-classification')
    users = Identity.IdentityManager(
        path ='./resources/json/identities.json',
        user=input("Welcome to the Auction House Front Desk!\n" \
        "Please enter your name (6 char max): ")[0:6])
    items = Transaction.TransactionManger(path ='./resources/json/items.json', identity=users)
    intentManager = Intent.IntentManager(
        intent_matcher=intentMatch, qa_searcher=QA,
        identity=users, transaction=items)
    eventManager = Event.EventManager(users, items)

    
    if users.newUser: intentManager.intent_tutorial() # ask new users if they want to do the tutorial

    while True:
        eventManager.print_events() # show user their events if any
        # print(items.remove_item("pspap"))    
        
        # event loop should go at start
            # instantly notify if the user switches identity
        eventManager.queue_event()

        # write to JSON after potential events
        users.write_json()
        items.write_json()

        users.exile_user_check()

        if(intentManager.intentFrozen['state']):
            if intentManager.intentFrozen['intent'] in intentManager.transactionIntents:
                # print(sub_intent)
                intent = 'transaction'
            else:
                intent = intentManager.intentFrozen['intent']
        else:
            user_input = intentManager.spellcheck(input("Please enter your prompt: ")) 
            
            # if sentence contains 'and'
                # too much information
                    # ask for more important     
            intentManager.disambiguation(user_input)
            
            # intent getting process
                # always handle question answering first, cases where questions are matched perfectly and the intent is something else will be rare
                    # this means three tiered input is first
                    # hence handle all the other intents first too     
            
            if user_input != None: # if the user has input something

                intent, score = intentMatch.search_intent(user_input) # match their intent using cosine sim (score is best score)
                intent = intentManager.three_tiered_confidence(intent=intent, score=score, is_transaction=False) # use score in three tiered input to determine confirmation technique
            else: # in case that three tiered fails, fallback on synonym resolution 
                intent = ""

            if intent == "": # following failure of three tiered
                for keyword in intentManager.transactionIntents: # three tiered is more specific to small talk | synoynm resolution allows for transaction intents to be matched with nltk data
                    sub_intent = intentManager.synonym_resolution(keyword, user_input)

                    if sub_intent != None: # if synonym resolution matches, force the transaction intent
                        # print(sub_intent)
                        intent = 'transaction'
                        break
                    
                

                if intentManager.intentHistory[len(intentManager.intentHistory)-2] == intent:
                    intentManager.intent_settings() # edge case where exit is already appended, then calls get_prev leading to a double notice call --------------------------------
                
                sleep(1) # prevent instant reply to slow down pace, preventing user overwhelm
            
            # sentiment analysis
            intentManager.sentiment_mood(user_input)
            
            # print(intentManager.intentHistory) # press enter (match '') to see intent history


        match intent:
            
            # Universal cases (all cases are universal)
            case 'exit':
                intentManager.intent_exit()
            case 'help' | 'tutorial':
                intentManager.intent_help()
            case 'greeting':
                intentManager.intent_greeting()
            case 'name-calling':
                intentManager.intent_name_calling()
            case 'question-greeting':
                intentManager.intent_question_greeting()
            case 'discoverability':
                intentManager.intent_discoverability()
            case 'question-answering': # Case for questions
                intentManager.intent_qa(question=user_input)
            case 'transaction' | 'auction':
                intentManager.intent_transaction(intent=sub_intent)


            # case '': # handling 'no' in three tiered | # this causes no input to get no response -> how does the user recover?
            #     pass
            case _: # default case handles the above issue
                print(f"I didn't quite get that {users.jsonUsers[users.currentUser]['nickname']}")
        

        # unfreeze frozen intent (frozen means the intent will repeat next iteration)
        if('unfreeze' in intentManager.intentHistory): # if unfreeze is in list (appended prev iteration) then queue the unfreeze
            # print("REMOVE PAIR THEN ---")
            # remove both freeze and unfreeze, causing neither to be in list
            
            intentManager.intentHistory.remove('unfreeze')
            intentManager.intentHistory.remove('freeze')
            
            if('freeze' not in intentManager.intentHistory): # if there isn't a freeze then we didn't freeze again (back to back repeats)
                # print("UNFREEZE")
                
                intentManager.unfreeze_intent() # hence we totally unfreeze the system
            else: # if there is a remaining freeze in the list then we re-called freeze this iteration
                # print("FREEZE AGAIN")
                
                intentManager.intentHistory.append('unfreeze')  # hence we append an unfreeze to make it a pair / queue the unfreeze next iteration
        elif(intentManager.intentHistory.count("freeze") == 1): # checking for one 'freeze' instance prevents 'unfreeze' being appended multiple times
            # print("FORZEN")
            
            intentManager.intentHistory.append('unfreeze')
                

if __name__ == "__main__":
    main()