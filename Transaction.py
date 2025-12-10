import json, random
from Identity import Identity

class Transaction:
    def __init__(self, path:str, identity:Identity):
        self.path = path
        self.users = identity # use to assign name of user when buying

        self.json = {}
        self.json_items = {}
        self.items_titles = []

        self.read_json()

    def read_json(self):
        with open(self.path, encoding ='utf8 ', errors ='ignore ', mode ='r') as json_file:
            self.json = json.load(json_file)
        self.json_items = self.json['items'] # list of items for sale from json

        self.items_titles = [x for x in self.json["items"]]

    def write_json(self):
        with open(self.path, encoding ='utf8 ', errors ='ignore ', mode ='w') as json_file:
            json.dump(self.json, json_file, indent=2)
        self.items_titles = [x for x in self.json["items"]]

        self.read_json()

    def constrain_num_input(self, prompt:str, range:tuple[int,int], int_float:bool): # input constraints / sanity checking --------------------------------------
        # sanity checking for numbers
            # ensure it is a number
            # ensure it is between bounds, pass a range tuple to constrain
                # insane idea if range doesn't work
                    # if num greater than range then cap
                    # if num less than range the also cap
                    # but we want to notify the user, not force them --------------------------------------------------------------
                
        try:
            num = float(input(prompt))
            
            if(int_float):
                num = int(num)
            else:
                num = float(f"{num:.2f}")
            print(num)
            # if num not in range(range): --------------------------------------------------------
            #     print("That number isn't in the specified range! ")
            #     return 0
        except:
            print("That isn't a number!")
            return 0
        
        return num

    def check_item_exists(self, title:str):
        if title in self.items_titles:
            return True
        return False
        
    def print_items(self, titles:list[str]):
        # in an ideal world: ----------------------------------------------------------------------
            # multiple pages: print(page x/10)
                # generators
                    # too complicated idk? --------------------------------------------------------
                    # literally just yield keyword, lock in
                # possible inputs: next/exit
                    # need an exit state to leave the page input

        # hence display the user's nickname so they can see if buying from self ------------------
        # also display risk --------------------------------------
        spacing = ' '*4
        print(f"Title:{spacing}Price:{spacing}Count:{spacing}Seller:{spacing}RISK:")
        for key, values in self.json_items.items():
            if key in titles:
                print('{title:<{title_width}}{spacing}{price:>{price_width}}{spacing}{count:>{count_width}}{spacing}{seller:>{seller_width}}{spacing}{risk:>{risk_width}}'.format( # this formatting should be used to limit input ---------------
                    spacing = spacing,
                    title = key, title_width = len('Title:'),
                    price = '£'+str(values["price"]), price_width = len('Price:'),
                    count = values['count'], count_width = len('Count:'),
                    seller = values['seller'], seller_width = len('Seller:'),
                    risk = values['risk'], risk_width = len('RISK:')
                    ))

            # yield, # enumerate to a total number of items (if x = 5: yield) (nothing to return)
    
    def create_item(self, user:str, title:str, price:int, count:int, bidding:bool):
        item = {
            'price': price,
            'count': count,
            'bidding': bidding,
            'seller': user,
            'buyer': '', # let the seller know who bought / bidded last on an item 
            'risk': 1 # risk always starts from 1, increments by one each unsuccessful steal (greater risk is worse)
        }

        # append to json
        self.json_items[title] = item
        self.write_json()
        
        # return True # no need to return success, we constrain items that get here so they are always successful

    def remove_item(self, title:str):
        if title in self.items_titles:
            item = self.json_items.pop(title)
            self.write_json()
            
            return item

    def write_transaction(self, user_title:str, event_prompt:str):
        if(self.users.check_user_exists(user_title)):
            self.users.json_users[user_title]["events"].append(event_prompt)

    # Transaction Methods -------------------------------------------------------------------------
        # these are intents but not in the same way as in the intent file
            # primarily mapped to using synonym resolution as there are only so many ways to say buy/sell that don't outright use the word (synonyms)
                # dict of synonyms for each intent
                # match intent by checking dict
            # can't break out of their dialogue tree
                # mostly because of circular imports with the Intent class...
                
    def buy(self):
        # return list of available items to buy
            # keyword to go to next page (using yield so sequential) ------------------------------
        self.print_items(self.items_titles)


        # input("Which item would you like to buy?: ")
            # conversational design: timelines, etc ------------------------------------
            # match item in self.items
                # if not in items match three tiered input using their input
            # self.json_items[item]['buyer'] = self.users.current_user
        buy_title = input("Which item would you like to buy?: ")        
        if not self.check_item_exists(buy_title):
            print(f"No match found for {buy_title}")
            return

        # if the user chooses to buy an item under their name, make a weird comment -------
            # they can't buy it as otherwise (currently) infinite money glitch
                # this is as they can list for whatever but we don't currently have a money system
                # or an inventory system

        # how many of item would you like to buy --------------------------------------------------
        buy_count = self.constrain_num_input(f"How many of {buy_title} would you like to buy?: ", [1, self.json_items[buy_title]['count']], int_float=0)
        if buy_count == 0: return
        elif buy_count > self.json_items[buy_title]['count']:
            print(f"There is not enough stock for {buy_count} of {buy_item}")
            return

        # check user's balance and let them know if they can purchase
        buy_price = self.json_items[buy_title]['price']
        buy_price_total = buy_count * buy_price
        if buy_price_total > self.users.json_users[self.users.current_user]['balance']:
            print(f"You can't afford to buy {buy_title}")
            return

        # reduce users balance by amount
        self.users.json_users[self.users.current_user]['balance'] -= buy_price_total
        
        # increase seller's balance by amount
        current_seller = self.json_items[buy_title]['seller']
        if current_seller != 'oracle':
            self.users.json_users[current_seller]['balance'] += buy_price_total


        # check total and change_item to reduce it by buy_count
            # if remaining total = 0 remove item
        self.json_items[buy_title]['count'] -= buy_count
        if self.json_items[buy_title]['count']  == 0: buy_item = self.remove_item()
        
        # write to buyer in item
        # write event to user storage
            # to let other users know if their items have been bought somehow
            # personalise in some way ------------------------------------------------
        buy_prompt = f"{self.users.current_user} has bought {buy_count} {buy_title}(s) for {buy_price_total}"
        self.write_transaction(current_seller, buy_prompt)        
  
        

    def sell(self):
        # return list of items currently being sold by the user
            # have intents based on whether they want to sell a new one or amend a listing
                # if selling
                    # ask if they want to sell flat or allow for biddings
                        
        # constrain length of selling names -------------------------------------------------------
        # did you mean x ---------------------
            # yes, cool spellcheck stuff
            # no, ok regardless
        item_title = input("What would you like to sell?: ")
        
        # check if item already exists ------------------------------------------------------------------
            # respond with the fact that it already does
                # including price as potential incentive for the user


        item_price = self.constrain_num_input(f"How much would you like to sell {item_title} for? (1-100): £", range=(1,100), int_float=False)
        if not item_price: return {}
        item_count = self.constrain_num_input(f"How many {item_title}'s would you like to sell?: (1-10): ", range=(1, 10), int_float=True)
        if not item_count: return {}
        
        partial_item = {
            'title': item_title,
            'price': item_price,
            'count': item_count,
        }
        print(partial_item)
        return partial_item

    def bid(self):
        # allow users to bid on items with the bidding flag as true
            # ask them how much they want to bid
                # restrict based on the money they currently have
        bid_item_titles = []
        for title in self.items_titles:
            if self.json_items[title]['bidding'] == True:
                bid_item_titles.append(title)

        self.print_items(titles=bid_item_titles)
        
        bid_title = input("Which item would you like to bid on?: ")        
        if not self.check_item_exists(bid_title) or bid_title not in bid_item_titles:
            print(f"No match found for {bid_title}")
            return

        bid_amount = self.constrain_num_input(f"How much do you want to bid (1-100) £{self.json_items[bid_title]['price']}+", range=(1,100), int_float=False)
        if not bid_amount: 
            print("Bid Failed...")
            return
        # elif user_is_poor # user has to be able to afford to buy ----------------------------------------------

        # {.2f} formatting again, see if it works ---------------------------------------------------------------
        price_before = self.json_items[bid_title]['price']
        self.json_items[bid_title]['price'] += bid_amount
        price_after = self.json_items[bid_title]['price']

        # write to user who is selling item
            # should also be writing to the person that last bidded
        bid_seller = self.json_items[bid_title]['seller']
        bid_buyer_old = self.json_items[bid_title]['buyer']
        bid_buyer_new =  self.users.current_user   

        if bid_buyer_old != '': # if there are bids
            # need to notify the now previous bidder
            self.write_transaction(bid_buyer_old,f"You were outbid on {bid_title} by {bid_buyer_new}. The new price is {price_after}")
        
        # always notify the seller of the bid, and update bidder
        self.json_items[bid_title]['buyer'] = bid_buyer_new
        self.write_transaction(bid_seller, f"Your {bid_title} has been bid on. The price is now {price_after}")
                
        print(f"Bid successful, the price of {bid_title} changed from £{price_before} to £{price_after}")

    def bounty(self):
        # check for people with status = criminal
            # return list and associate price
                # can't really get bounties, no way to catch a criminal
                    # queuing with events
                        # user can see a criminal as an event, and have the option to stop them
                            # get money, remove criminal from bounty board
        
        criminal_names = []
        for name in self.users.user_names:
            if self.users.json_users[name]['status'] == 'criminal':
                criminal_names.append(name)
                
        if criminal_names == []:
            print("There are currently no bounties")

        self.users.print_users(criminal_names)
  
    def search_item(self, title=str):
        if not self.check_item_exists(title):
            print(f"{title} is not listed here")
        
        self.print_items(titles=[title])

    def steal(self): # risk based on item
        # if doing no inventory (prototype): "you sold x elsewhere, gaining £££"
        self.print_items(self.items_titles)

        # ask user if they want to steal item
        steal_title = input("Which item do you want to steal?\nYou: ")
        
            # update risk of item (for everyone)
            # random number between 1 and n
                # risk from 0 to 5
                    # where we take 2 to power of risk
                        # if random randint(1, 2^risk) = 1
                            # get caught bozo
            # risk / 16
            # risk / 8
            # risk / 4
            # risk / 2
            # risk / 1
        
        # risk is 1 to 5, with 1 being the least (when visible to the user)
            # we take the inverse
            # zero isn't the least as 0 risk implies no risk, there is always risk here
        
        item_risk = self.json_items[steal_title]['risk']
        steal_risk = 5 - (self.json_items[steal_title]['risk'] - 1)
        steal_chance = random.randint(1, pow(2, steal_risk))

        if steal_chance == 1:
            # On fail change system-mood
            # mood goes down by
            self.users.json_users[self.users.current_user]['system-mood'] -= float(item_risk)/10
            self.users.json_users[self.users.current_user]['status'] = 'criminal'
            print("You were caught\nYou failed...")
            return

        # On success
        
        # Increment displayed risk (universally for everyone)
        if item_risk < 5: self.json_items[steal_title]['risk'] +=1
        else: pass
        
        # Decrement count of item
        steal_item_count = self.json_items[steal_title]['count']
        if steal_item_count > 0: self.json_items[steal_title]['count'] -=1
        else: self.remove_item(steal_title)

        # increment user balance
        steal_price = steal_item_count * self.json_items[steal_title]['price']
        self.users.json_users[self.users.current_user]['balance'] += steal_price
        print(f"You stole {steal_title} elsewhere for {self.json_items[steal_title]['price']} profit")
        
        # write to output
            # user who sold has now lost money
        self.write_transaction(self.json_items[steal_title]['seller'], f"{self.users.current_user} stole a {steal_title}")
        pass

    def secret(self):
        print("Psst... speech is ephemeral... you heard nothing...")

    # Not implemented
    def change_listing(self): 
        # return list of items the user has up for sale
        user_items = []
        
        for key, values in self.json_items.items():
            if values['seller'] == self.users.current_user:
                user_items.append(key)
        
        self.print_items(user_items)

        item_change = input("Which of your items would you like to change?: ")

        if item_change not in user_items:
            print("That item is not one of your listings")

        # changes include
            # adding item # self.limits[0] or something for total: self.limits = (1, 100)
            # removing item # same as above
            # turn bidding on and off

        # match input(""): # need 'synonym resolution' match-case
        #     case '':
        #         pass
        #     case 'bidding':
        #         pass
        #     case 'remove':
        #         pass