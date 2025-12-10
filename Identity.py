import json, sys
from time import sleep

class Identity:
    def __init__(self, path:str, user:str):
        self.path = path

        self.json = {}
        with open(self.path, encoding ='utf8 ', errors ='ignore ', mode ='r') as json_file:
            self.json = json.load(json_file)#['users']#[0]
        self.json_users = self.json['users']

        self.user_names = [x for x in self.json["users"].keys()] # list of registered users from json
        print(self.user_names)
        self.current_user = ''
        self.new_user = not self.check_user_exists(user)

        self.load_user(user)
        if self.check_exile(self.current_user):
            print("Do not come back")
            sys.exit()
        # self.user_statuses = ['criminal', 'neutral', 'law-abiding']
        # self.chatbot_moods = ['happy', 'sad', 'angry']

    def write_json(self):
        with open(self.path, encoding ='utf8 ', errors ='ignore ', mode ='w') as json_file:
            json.dump(self.json, json_file, indent=2)
        # no need to load json after as self.json is equal to file contents

    def print_users(self, names:list[str]):
        spacing = ' '*4
        print(f"Name:{spacing}Bounty:{spacing}")
        for key, values in self.json_users.items():
            if key in names:
                print('{name:<{name_width}}{spacing}{bounty:>{bounty_width}}{spacing}'.format( # this formatting should be used to limit input ---------------
                    spacing = spacing,
                    name = key, name_width = len('Name:'),
                    bounty = '£'+str(values["bounty"]), bounty_width = len('Bounty:'),
                    ))

    def create_user(self, name:str):
        if self.check_user_exists(name):
            return False # unsuccessful

        self.user_names.append(name)
        user = {
            'nickname': 'champ', # allow changing of nickname -------------------------------------
            'status': 'neutral', # exile, criminal, neutral, law-abiding
            'balance': 1000,
            'bounty': 0,
            'system-mood': 0.5, # changed to 0 to 1 range
            'events': []
            # could technically double store data by directly storing listings --------------------
                # currently only function that needs user items is change_listing
                    # if enough time then yea sure change it
            # inventory:
        }
        
        # append to json
        self.json_users[name] = user
        self.write_json()
        
        return True # successful

    def load_user(self, user:str):
        
        if not self.check_user_exists(user):
            self.create_user(name=user)  
        
        self.current_user = user

    def check_user_exists(self, user:str):
        if user in self.user_names:
            return True
        return False

    def change_current_user_status(self, status:str):
        self.json_users[self.current_user]['status'] = status
        self.write_json()
    
    def check_exile(self, user_title:str):
        if self.json_users[user_title]['status'] == 'exile':
            return True
        return False
    
    def exile_user(self): # user is blocked on entry
        if self.json_users[self.current_user]['system-mood'] == 0:
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
        
        current_mood = self.json_users[self.current_user]['system-mood'][mood]
        current_mood += change
        
        if current_mood < 0: current_mood = 0
        elif current_mood > 1: current_mood = 1

        self.write_json()

    def get_greatest_chatbot_mood(self):
        chatbot_moods = self.json_users[self.current_user]['system-mood']
        return max(chatbot_moods, chatbot_moods.get)

    def get_average_chatbot_mood(self):
        mood_total = 0.0
        num_moods = 0.0

        for value in self.json_users[self.current_user]['system-mood'].values():
            mood_total += value
            num_moods += 1

        return mood_total/num_moods
    
    def get_chatbot_mood(self, mood:str):
        
        if mood in self.chatbot_moods:
            return self.json_users[self.current_user]['system-mood'][mood]
        
        return ''