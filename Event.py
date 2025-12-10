import random

from nltk.corpus import words, wordnet as wn

from Identity import IdentityManager
from Transaction import TransactionManger



class EventManager: # manages events that can occur in the auction house
    # create event object in main, run it n times an iteration
        # don't make it annoying to the user
    def __init__(self, users:IdentityManager, items:TransactionManger):
        # load stat from user
        # load json for shop / bounties

        self.users = users
        self.items = items

    

    def print_events(self):
        '''Prints the strings listed in the current user's event list from JSON'''
        # when a user logs in, update them of anything related to them
            # read their events and empty them
            # needs to be staggered and limited so user isn't overwhelmed --------------------
                # pass intent and use staggered output
                # staggered output in main file
        current_user_events: list[str]
        current_user_events = self.users.jsonUsers[self.users.currentUser]['events']
        
        if current_user_events != []:
            for x in current_user_events:
                # colour to indicate positive negative -----------------------------------------
                    # sentiment analysis
                print("Notice: "+x)
                current_user_events.remove(x)
        pass

    def queue_event(self):
        '''Selects a random event'''

        x = random.randint(1,5)

        if x == 1:
            self.event_buy()
        elif x == 2:
            self.event_sell()


    def event_buy(self):
        '''Simulates a buy transaction, using the 'oracle' entity'''
        # buy from a user current user, decrementing count of thing
            # if user is current user, notify them on next iteration
        if self.items.itemsTitles == []:
            return

        buy_title = random.choice(self.items.itemsTitles)
        
        if self.items.jsonItems[buy_title]['seller'] == 'oracle':
            return

        buy_item = self.items.jsonItems[buy_title]
        buy_seller = self.items.jsonItems[buy_title]['seller']
        
        
        # buy random count of item
        buy_count = random.randint(1, buy_item['count'])
        buy_price = self.items.jsonItems[buy_title]['price']
        buy_price_total = buy_count * buy_price

        # pay money to user
        current_seller = self.items.jsonItems[buy_title]['seller']
        self.users.jsonUsers[current_seller]['balance'] += buy_price_total
        
        # buy item
        self.items.jsonItems[buy_title]['count'] -= buy_count
        
        # remove item if no more remain
        if self.items.jsonItems[buy_title]['count']  == 0: buy_item = self.items.remove_item(buy_title)        

        # format string
        buy_prompt = f"oracle has bought {buy_count} {buy_title}(s) for {buy_price_total}"
        self.items.write_transaction(buy_seller, buy_prompt)
        print("bought")

    def event_sell(self):
        '''Simulates a sell transaction, using the 'oracle' entity'''
        # create new listing for the user to buy
            # random item name (from where)
                # two random words from wordnet        
        sell_title = random.choice(words.words())[0:5]

        # random price 1-100
        sell_price = random.randint(1,100)

        # random count 1-100
        sell_count = random.randint(1,100)
        
        # random bidding
        sell_bid = random.randint(0,1)
        
        # seller
        self.items.create_item('oracle', sell_title, sell_price, sell_count, sell_bid)
        # risk

    # Unfinished, not enough time :(

    def event_bid(self):
        # bid on a random listing
            # increase the price of a random listing

        # choose random item

        # choose random amount (1-100)

        # update bid for that item

        pass
    
    def event_sell_bid():
        # last_bid flag on item to track who last bidded it
        # sell to whoever last bid (current buyer)
        # how do we determine when bid expires
            # a: random because no time rn 
            # b: clock cycle in main loop ---------------------------------------------------------
                # needs to account for all possible routes
                    # put at start
                # this would also need to be in storage
                # issue is that we now have two vars used to identify bidding
                # instead make the check for bidding if clock != 0
        # issue
            # if we sell to a user that no longer has the balance
            # not enough time to solve
        pass

    def event_bounty(self): # this prompts the user finding a person
        # if the user has looked at the bounty board
            # they find random user
                # they have the choice to accuse them of having a bounty
                    # pay up if ur wrong
                    # gain the bounty if correct

        # random person from bounty board
        
        # prompt user, do you want to turn them in?
            # user has to know the bounty board
        
        # gain money if correct

        # lose money if incorrect

        pass

    def event_steal(self): # if we have the time make new 
        # literally decrease an item and say it was stolen
            # money lost, goes nowhere sadge

        # steal based on risk like in Transactino
        pass