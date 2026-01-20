import json, sys
from time import sleep

class IdentityManager:
    def __init__(self, path:str, user:str):
        self.path = path

        self.json = {}
        self.jsonUsers = {}

        self.userNames = [] # list of registered users from json
        self.read_json()
        
        self.newUser = not self.check_user_exists(user)

        self.currentUser = ''
        self.load_user(user)
        if self.check_exile(self.currentUser):
            print("Do not come back")
            sys.exit()
        
        # self.user_statuses = ['criminal', 'neutral', 'law-abiding']

    def read_json(self):
        '''Reads the JSON file responsible for storage'''
        with open(self.path, encoding ='utf8 ', errors ='ignore ', mode ='r') as json_file:
            self.json = json.load(json_file)#['users']#[0]
        self.jsonUsers = self.json['users']

        self.userNames = [x for x in self.json["users"].keys()]

    def write_json(self):
        '''Updates the Identity JSON file in storage.'''
        with open(self.path, encoding ='utf8 ', errors ='ignore ', mode ='w') as json_file:
            json.dump(self.json, json_file, indent=2)

        self.read_json()

    def print_users(self, names:list[str]):
        '''Displays users and their bounties'''
        spacing = ' '*4
        print(f"Name:{spacing}Bounty:{spacing}")
        for key, values in self.jsonUsers.items():
            if key in names:
                print('{name:<{name_width}}{spacing}{bounty:>{bounty_width}}{spacing}'.format( # this formatting should be used to limit input ---------------
                    spacing = spacing,
                    name = key, name_width = len('Name:'),
                    bounty = '£'+str(values["bounty"]), bounty_width = len('Bounty:'),
                    ))

    def create_user(self, name:str):
        '''Creates a user entry in memory using a 'name' key. Fails if key already exists'''
        if self.check_user_exists(name):
            return False # unsuccessful

        self.userNames.append(name)
        user = {
            'nickname': 'champ', # allow changing of nickname -------------------------------------
            'status': 'neutral', # exile, criminal, neutral, law-abiding
            'balance': 1000,
            'bounty': 0,
            'system-mood': 0.5, # 0 to 1 range (0 bad)
            'events': []
            # inventory:
        }
        
        # append to json
        self.jsonUsers[name] = user
        self.write_json()
        
        return True # successful

    def load_user(self, user:str):
        '''Replaces the current user with a newly specified user'''
        if not self.check_user_exists(user):
            self.create_user(name=user)  
        
        self.currentUser = user

    def check_user_exists(self, user:str):
        '''Determines if a user key exists in JSON storage'''
        if user in self.userNames:
            return True
        return False

    def change_current_user_status(self, status:str):
        '''Changes the status of the current user to a specified status'''
        self.jsonUsers[self.currentUser]['status'] = status
        self.write_json()
    
    def check_exile(self, user_title:str):
        '''Determines if the user has the exile status'''
        if self.jsonUsers[user_title]['status'] == 'exile':
            return True
        return False
    
    def exile_user_check(self): # user is blocked on entry
        '''Handles the case if a user has been exiled. They are not allowed entry.'''
        if self.jsonUsers[self.currentUser]['system-mood'] == 0:
            print("About time you saw the consequences of your actions")
            print("The Auction House always wins")
            print("Do not come back")
            self.change_current_user_status('exile')
            sys.exit()
            
    # deprecated, mood is now singular ------------------------------------------------------        

    def update_chatbot_mood(self, mood:str, positive:bool):

        change = 0.1
        if not positive :
            change = -0.1
        
        current_mood = self.jsonUsers[self.currentUser]['system-mood'][mood]
        current_mood += change
        
        if current_mood < 0: current_mood = 0
        elif current_mood > 1: current_mood = 1

        self.write_json()

    def get_greatest_chatbot_mood(self):
        chatbot_moods = self.jsonUsers[self.currentUser]['system-mood']
        return max(chatbot_moods, chatbot_moods.get)

    def get_average_chatbot_mood(self):
        mood_total = 0.0
        num_moods = 0.0

        for value in self.jsonUsers[self.currentUser]['system-mood'].values():
            mood_total += value
            num_moods += 1

        return mood_total/num_moods
    
    def get_chatbot_mood(self, mood:str):
        
        if mood in self.chatbotMoods:
            return self.jsonUsers[self.currentUser]['system-mood'][mood]
        
        return ''