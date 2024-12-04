from .ext import Database as DB
from .bank_funcs import Bank
from .inventory_funcs import Inventory
from .responses_funcs import Responses


__all__ = [
    "Database"
]


class Database(DB):
    """
    Database module class.
    
    Grabs model classes from other `modules` files to add to self, making them accessible
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bank = Bank(self)
        self.inv = Inventory(self)
        self.resp = Responses(self)
