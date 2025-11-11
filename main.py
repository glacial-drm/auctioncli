from time import sleep
import Search
from joblib import load
# from Intent import classify_text

def main():
    name = ""
    c = Search.CSV_QA(path='../COMP3074-CW1-Dataset.csv')
    # clf = load("../objects/log_reg_clf.joblib")
    # print(classify_text(clf, "help"))
    
    while True:
        user_input = input("Text goes here: ")
        sleep(1)

        match user_input.lower():
            case 'exit':
                print("Goodbye!")
                break

            case 'help': # Print helpful information -----------
                print("Help is on the way! (adding help command closer to completion)")
            

            # USE LAB 2 TO CLASSIFY TEXT IN TERMS OF INTENT --------------------
            case 'hi' | 'hello': # Case for greetings(?)
                if(name):
                    print(f"Hello {name}")
                else:
                    name = input("Hello, what is your name? ")
                    print(f"Nice to meet you {name}")

            case 'what is my name' | 'what is my name?':
                if(name):
                    print(f"Your name is {name}")
                else:
                    print("You haven't told me your name yet...")
            
            case 'how are you' | 'how are you?':
                ip = input("I am fine, how are you? ")
                match ip: # Possibly do some sentiment analysis ------------
                    case '':
                        print("Not one for small talk I see")
                    case _:
                        print("That's nice, or maybe it isn't...")

            case 'what can you do' | 'what can you do?':
                print("I can meet all the criteria for the checkpoint :)")

            case _: # Case for questions
                answers = c.search_qa(query=user_input)
                
                if(answers):
                    for ans in answers:
                        print(ans)                    
                else: # Case for if we can't understand input (LAST CASE)
                    print("I'm sorry, I didn't understand that. Please use the 'help' command for assistance.")

if __name__ == "__main__":
    main()