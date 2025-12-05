from time import sleep
import Search
import Intent
import nltk

def main():
    # we need a start to concretely load any external files
    # if user exists then load
    # else instantiate
    name = ""

    c = Search.CSV_QA(path='./resources/COMP3074-CW1-Dataset.csv')
    d = Search.TXT_Intent(folder_path='./resources/intent-classification')
    e = Intent.Intent(intent_searcher=d, qa_searcher=c)
    transaction_keywords = ['auction', 'buy', 'sell', 'bounty', 'purchase'] # make a file for, further refine by then checking word in prompt
    
    while True:
        user_input = input("Text goes here: ")
        sleep(1)

        if any(substring in user_input for substring in transaction_keywords): # make a file for, further refine by then checking word in prompt
            print("address me")

        # intent, score = d.search_intent(user_input) # we also need three tiered confidence
            # 0.9 | 0.7 | less

        match user_input: # intent: # d.classify_text(user_input):
            case 'exit':
                e.intent_exit()
            case 'help':
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
            # no default case as classifier doesn't return default
                # implement three tiered function, using default?

if __name__ == "__main__":
    main()