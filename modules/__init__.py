from .ext import Database as DB
from .bank_funcs import Bank
from .inventory_funcs import Inventory
from .responses_funcs import Responses #, Responses_Debug_Settings


__all__ = [
    "Database"
]


class Database(DB):
    """
    Database module class. Found within `modules/__init__.py`
    
    Grabs model classes from other `modules` files to add to self, making them accessible
    
    Ported from Economy Bot and retooled for BraxCord
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #self.bank = Bank(self)
        #self.inv = Inventory(self)
        #self.r_verb = Responses_Debug_Settings(True, True, True)
        self.resp = Responses(self, v4=False, v3=False) #, self.r_verb)
