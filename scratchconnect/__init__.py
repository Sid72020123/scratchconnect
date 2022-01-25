__name__ = "scratchconnect"
__version__ = "2.4.2"
__author__ = "Siddhesh Chavan"
__documentation__ = "https://sid72020123.github.io/scratchconnect/"
__doc__ = f"""
scratchconnect is a Python Library to connect Scratch API and much more.
This library can show the statistics of Users, Projects, Studios, Forums and also connect and set cloud variables of a project!
Import Statement:
    import scratchconnect
Documentation(Tutorial):
    For documentation, go to {__documentation__}
Required Libraries:
    requests*, re*, json*, time*, threading*, websocket-client
    * -> In-built
    This library also uses pyEmmiter to handle cloud events in Python.
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
    15/07/2021(v1.0) - First Release!
    18/07/2021(V1.1) - Made the 'studio.get_projects()'.
    19/07/2021(v1.2) - Made the get comments, curators, managers of the studio
    13/08/2021(v1.3) - Added the get comments function
    14/08/2021(v1.4) - Updated the get messages function
    17/08/2021(v1.5) - Made some bug fixes
    18/09/2021(v1.7) - Made the ScratchConnect and User Classes fast and Improved methods
    19/09/2021(v1.8) - Made the Studio Class Faster and Improved methods
    25/09/2021(v1.8.5) - Updated the Project and User classes
    02/10/2021(v2.0) - Updated the Cloud and Forum Class
    10/10/2021(v2.0.1) - Fixed some cloud stuff
    11/10/2021(v2.1) - Added some features to Forum Class
    24/10/2021(v2.1.1) - Started making the scStorage Class
    29/10/2021(v2.1.1.1) - Fixed set_bio() and set_work() and updated the scDataBase
    30/10/2021(v2.2.5) - Updated the scStorage
    31/10/2021(v2.2.7) - Updated the scStorage
    25/11/2021(v2.3) - Updated the scStorage and CloudConnection
    13/12/2021(v2.3.5) - Started making the TurbowarpCloudConnection feature and added some methods to it
    14/12/2021(v2.4) - Updated and fixed mistakes in docs
    09/01/2022(v2.4.1) - Code Fixes
    25/01/2022(v2.4.2) - Added new Comment API
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
