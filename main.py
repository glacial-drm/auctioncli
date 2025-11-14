from time import sleep
import Search
import Intent
from joblib import load

def main():
    name = ""
    c = Search.CSV_QA(path='../COMP3074-CW1-Dataset.csv')
    d = Intent.Intent_Classifier()
    d.build_log_reg_clf()
    
    while True:
        user_input = input("Text goes here: ")
        sleep(1)

        match d.classify_text(user_input):
            case 'exit':
                print("Goodbye!")
                break

            case 'help': # Print helpful information -----------
                print("Help is on the way! (adding help command closer to completion)")
            

            # USE LAB 2 TO CLASSIFY TEXT IN TERMS OF INTENT --------------------
            case 'greeting':
                if(name):
                    print(f"Hello {name}")
                else:
                    name = input("Hello, what is your name? ")
                    print(f"Nice to meet you {name}")

            case 'name-calling':
                if(name):
                    print(f"Your name is {name}")
                else:
                    print("You haven't told me your name yet...")
            
            case 'question-greeting':
                ip = input("I am fine, how are you? ")
                match ip: # Possibly do some sentiment analysis ------------
                    case '':
                        print("Not one for small talk I see")
                    case _:
                        print("That's nice, or maybe it isn't...")

            case 'discoverability':
                print("I can meet all the criteria for the checkpoint :)")

            # somehow check if words are in corpus beforehand, otherwise zero-divis

            case 'question-answering': # Case for questions
                answers = c.search_qa(query=user_input)
                
                if(answers):
                    for ans in answers:
                        print(ans)                    
                else: # Case for if we can't understand input (LAST CASE)
                    print("I'm sorry, I didn't understand that. Please use the 'help' command for assistance.")

            case _: # Default case no longer necessary, output is from set of labels
                print("I'm sorry, I didn't understand that. Please use the 'help' command for assistance.")

if __name__ == "__main__":
    main()