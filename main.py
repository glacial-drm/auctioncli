from time import sleep
import Search, Intent, Identity, Transaction, Event
import nltk

def main():
    # rename these more appropriately -------------------------------------------------------------
    c = Search.CSV_QA(path='./resources/COMP3074-CW1-Dataset.csv')
    d = Search.TXT_Intent(folder_path='./resources/intent-classification')
    f = Identity.Identity(
        path ='./resources/json/identities.json',
        user=input("Welcome to the Auction House!\n" \
        "Please enter your name (6 char max): ")[0:6])
    g = Transaction.Transaction(path ='./resources/json/items.json', identity=f)
    e = Intent.Intent(
        intent_matcher=d, qa_searcher=c,
        identity=f, transaction=g)
    h = Event.Event(f, g)

    
    
    if f.new_user: e.intent_tutorial()

    while True:
        h.print_events() # show user their events if any
        # print(g.remove_item("pspap"))    

        # write to JSON just in case I forgot it somewhere
            # would also need to go in repeat intent -------------------
            # maybe change approach
        f.write_json()
        g.write_json()



        # event loop should go at start -----------------------------------------------------------
            # identity switching should queue this as the next thing
            # as well as welcome back message


        if(e.intent_frozen['state']):
            if e.intent_frozen['intent'] in e.transaction_intents:
                print(sub_intent)
                user_input = 'transaction'
            else:
                user_input = e.intent_frozen['intent']
        else:
            user_input = e.spellcheck(input("You: ")) 
            
            # change to something meaniningful -----------------------------------------           
            # print(user_input)

            #  disambiguation   -------------------------------------------------------------------
                # if sentence contains and
                # too much information
                    # ask for one at a time
                        # freeze the next intent
                # too little information
                    # we already handle too little information (intent missing, not multiple options or omissions)


            # intent getting process
                # always handle question answering first, cases where questions are matched perfectly and the intent is something else will be rare
                    # this means three tiered intent is first
                    # hence handle all the other intents first too
                # in case that three tiered fails, fallback on synonym resolution 
            intent, score = user_input, 1#d.search_intent(user_input)
            
            intent = e.three_tiered_confidence(intent=intent, score=score, is_transaction=False)
            user_input = intent # temporary while we stop searching intent/qa because that takes a while (eventually replace this with three_tiered_input) ------------------------------
            
            
            for keyword in e.transaction_intents:
                sub_intent = e.synonym_resolution(keyword, user_input)
                
                if sub_intent != None:
                    print(sub_intent)
                    user_input = 'transaction'
                    break
                
            # sentiment analysis ----------------------------------------------------------------
            
            if e.intent_history[len(e.intent_history)-2] == user_input:
                e.intent_settings() # edge case where exit is already appended, then calls get_prev leading to a double notice call --------------------------------------------
            sleep(1) # . . . for thinking (spaced by sleep to look animated) # then replace with output -------------------------------------------------------------------------------
        print(e.intent_history) # press enter (match '') to see intent history


        match user_input: # intent: # d.classify_text(user_input):
            
            # Universal cases (all cases are universal)
            case 'exit':
                e.intent_exit()
            case 'help' | 'tutorial':
                e.intent_help()
            case 'greeting':
                e.intent_greeting()
            case 'name-calling':
                e.intent_name_calling()
            case 'question-greeting':
                e.intent_question_greeting()
            case 'discoverability':
                e.intent_discoverability()
            case 'question-answering': # Case for questions
                e.intent_qa(question=user_input)
            case 'transaction' | 'auction':
                e.intent_transaction(intent=sub_intent)


            case '': # handling 'no' in three tiered | what about regular -------------------------
                pass
            case _: # implement three tiered function, using default as explicit reprompt
                print(f"I didn't quite get that {f.json_users[f.current_user]['nickname']}")
        

        # unfreeze frozen intent (frozen means the intent will repeat next iteration)
        if('unfreeze' in e.intent_history): # if unfreeze is in list (appended prev iteration) then queue the unfreeze
            print("REMOVE PAIR THEN ---")
            # remove both freeze and unfreeze, causing neither to be in list
            e.intent_history.remove('unfreeze')
            e.intent_history.remove('freeze')
            
            if('freeze' not in e.intent_history): # if there isn't a freeze then we didn't freeze again (back to back repeats)
                print("UNFREEZE")
                e.unfreeze_intent() # hence we totally unfreeze the system
            else: # if there is a remaining freeze in the list then we re-called freeze this iteration
                print("FREEZE AGAIN")
                e.intent_history.append('unfreeze')  # hence we append an unfreeze to make it a pair / queue the unfreeze next iteration
        elif(e.intent_history.count("freeze") == 1): # checking for one 'freeze' instance prevents 'unfreeze' being appended multiple times
            print("FORZEN")
            e.intent_history.append('unfreeze')
                

if __name__ == "__main__":
    main()