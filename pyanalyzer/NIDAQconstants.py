# Create a list of constants
# Use these constants when calling functions (that way, changes to the underlying code won't break other people's code)
from enum import Enum

class coupling(Enum):
    AC = False
    DC = True

class excitation(Enum):
        ICP = True
        voltage = False