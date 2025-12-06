
class Transaction:
    def __init__(self):
        
        # load some json containing items
            # items can be added and removed
            # the store is consistent for everyone except for a few differences
                # the user can only buy other people's items
        self.items = {
            {
                'title': '',
                'price': 0,
                'seller': '',
                'buyer': '', # let the seller know who bought the item
            }
        }
        
    