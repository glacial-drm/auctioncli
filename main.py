from time import sleep
import Search, Intent, Identity
import nltk

def main():
    # we need a start to concretely load any external files
    # if user exists then load
    # else instantiate

    c = Search.CSV_QA(path='./resources/COMP3074-CW1-Dataset.csv')
    d = Search.TXT_Intent(folder_path='./resources/intent-classification')
    f = Identity.Identity(path ='./resources/json/identities.json',
                          user=input("Welcome to the Auction House!\nPlease enter your name: ")) # possibly verify user's name-----------------------------------------------
    e = Intent.Intent(intent_matcher=d, qa_searcher=c, identity=f)
    
    # implement spellcheck --------------------------------------------------
    
    transaction_keywords = ['auction', 'buy', 'sell', 'bounty', 'purchase', 'transaction'] # get into transaction 'state'
        # then pass found keyword into transaction
    


    # make input some prompt for user to respond to? ------------------------
        # make intent options clear using help function, call help first to make possible intents clear?
    e.tutorial()
    while True:
        if(e.intent_frozen['state']):
            user_input = e.intent_frozen['intent']
        else:
            user_input = input("You: ") #  can't use three_tier_input here as it doesn't keep track of output, which is needed for qa/transaction

            intent, score = user_input, 1#d.search_intent(user_input)
            intent = e.three_tiered_confidence(intent=intent, score=score, is_transaction=False)
            
            user_input = intent # temporary while we stop searching intent/qa because that takes a while

        sleep(1)
        
        # Transaction is currently gap filling ------------------------------
        if any(substring in user_input for substring in transaction_keywords): # make a file for, further refine by then checking word in prompt
            print("address me")

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
            case 'transaction':
                e.intent_transaction(intent=user_input) # pass intent as we map for multiple keywords
                    # cosine sim in files -----------------------------------
                    # specific intent for transaction, all keywords to do with transaction go there
                        # as well as gap filling (?) to show we did it


            case '': # handling 'no' in three tiered
                pass
            case _: # implement three tiered function, using default as explicit reprompt
                print(f"I didn't quite get that {e.nickname}")
                continue
        

        # unfreeze frozen intent --------------------------------------------
        e.unfreeze_intent()

if __name__ == "__main__":
    main()