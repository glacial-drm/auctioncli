import coursework.src.Identity as Identity

class Event: # manages events that can occur in the auction house
    # create event object in main, run it n times an iteration
    def __init__(self, user:Identity):
        # load stat from user
        # load json for shop / bounties
        pass

    def buy(self):
        # buy from the current user, decrementing count of thing
        pass
    def sell(self):
        # create new listing for the user to buy
        pass
    def bid(self):
        # bid on a random listing
        pass
    # def bounty(self): # we don't make new criminals...