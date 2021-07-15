__name__ = "scratchconnect"
__version__ = "0.1"
__author__ = "Siddhesh Chavan"
__documentation__ = "https://sid72020123.github.io/scratchconnect/"
__doc__ = f"""
scratchconnect is a Python Library to connect Scratch Programming Language and get the data from thr Scratch Website(https://scratch.mit.edu/)
scratchconnect uses Scratch-Api and the Scratch DB to get the data.
Import Statement:
    import scratchconnect
Documentation(Tutorial):
    For documentation, go to {__documentation__}
Required Libraries:
    requests*, re*, json*, time*, websocket, websocket-client
    * -> In-built
History:
    19/06/2021(v0.0.0.1) - First made the library and updated it.
    20/06/2021(v0.1) - Added many features.
    21/06/2021(v0.1.9) - Bug fixes.
    26/06/2021(v0.2.0) - Made Improvements and added new features.
    27/06/2021(v0.2.6) - Bug Fixes and update and made the 'Studio' class.
    03/07/2021(v0.4.5) - Added many functions and made the 'Project' class.
    04/07/2021(v0.5.0) - Update.
    05/07/2021(v0.5.1) - Updated the messages function.
    06/07/2021(v0.6.0) - Updated CloudConnection.
    08/07/2021(v0.7.5) - Updated CloudConnection.
    10/07/2021(v0.7.5) - Updated CloudConnection, made the Forum class and added DocString.
    13/07/2021(v0.9.7) - Added DocString.
    14/07/2021(v0.9.0) - Bug Fixes.
    15/07/2021(v0.1.0) - First Release!
Credits:
    All code by Siddhesh Chavan.
Information:
    Module made by:- Siddhesh Chavan
    Age:- 15 (as of 2021)
    Email:- siddheshchavan2020@gmail.com
    YouTube Channel:- Siddhesh Chavan (Link: https://www.youtube.com/channel/UCWcSxfT-SbqAktvGAsrtadQ)
    Scratch Account:- @Sid72020123 (Link: https://scratch.mit.edu/users/Sid72020123/)
    My self-made Website: https://Sid72020123.github.io/
"""

from scratchconnect.ScratchConnect import ScratchConnect
from scratchconnect import Exceptions

print(f"{__name__} v{__version__} - {__documentation__}")
