import json
from os.path import join

class Identity:
    def __init__(self, path:str, user:str):
        self.path = path
        
        self.json = {}
        with open(self.path, encoding ='utf8 ', errors ='ignore ', mode ='r') as json_file:
            self.json = json.load(json_file)#['users']#[0]
        self.json_users = self.json['users']

        self.users = [x['name'] for x in self.json["users"]] # list of registered users from json
        self.current_user = ''

        self.load_user(user)
        # self.user_statuses = ['criminal', 'neutral', 'law-abiding']
        # self.chatbot_moods = ['happy', 'sad', 'angry']

    def write_json(self):
        with open(self.path, encoding ='utf8 ', errors ='ignore ', mode ='w') as json_file:
            json.dump(self.json, json_file, indent=2)
        # no need to load json after as self.json is equal to file contents

    def create_user(self, name:str):
        if self.check_user_exists(name):
            return False # unsuccessful

        self.users.append(name)
        user = {
            'name': name,
            'status': 'neutral', # criminal, neutral, law-abiding
            'chatbot-mood': {  # 0 is min, 1 is max, keep it consistent or based on user, shows identity management
                'happy': 0.0,
                'sad': 0.0,
                'angry': 0.0
            }
        }
        
        # append to json
        self.json_users.append(user)
        self.write_json()
        
        return True # successful

    def load_user(self, user:str):
        
        if not self.check_user_exists(user):
            self.create_user(name=user)  
        
        self.current_user = user

    def check_user_exists(self, user:str):
        if user in self.users:
            return True
        return False

    # untested methods ------------------------------------------------------


    def update_user_status(self, status:str):
        self.json_users[self.current_user]['status'] = status
        self.write_json()

    def update_chatbot_mood(self, mood:str, positive:bool):

        change = 0.1
        if not positive :
            change = -0.1
        
        current_mood = self.json_users[self.current_user]['chatbot-mood'][mood]
        current_mood += change
        
        if current_mood < 0: current_mood = 0
        elif current_mood > 1: current_mood = 1

        self.write_json()

    def get_average_chatbot_mood(self):
        mood_total = 0.0
        num_moods = 0.0

        for value in self.json_users[self.current_user]['chatbot-mood'].values():
            mood_total += value
            num_moods += 1

        return mood_total/num_moods
    
    def get_chatbot_mood(self, mood:str):
        
        if mood in self.chatbot_moods:
            return self.json_users[self.current_user]['chatbot-mood'][mood]
        
        return ''