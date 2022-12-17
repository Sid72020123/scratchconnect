__name__ = "scratchconnect"
__version__ = "4.0.0"
__author__ = "Siddhesh Chavan"
__documentation__ = "https://sid72020123.github.io/scratchconnect/"
__doc__ = f"""
ScratchConnect is a Python Library to connect Scratch API and much more.
This library can show the statistics of Users, Projects, Studios, Forums and also connect and set cloud variables of a project!
Import Statement:
    import scratchconnect
Documentation(Tutorial):
    For documentation, go to {__documentation__}
Required Libraries:
    requests*, re*, json*, time*, traceback*, threading*, urllib*, PIL*, websocket-client
    * -> In-built
Optional Libraries:
    pyhtmlchart - For Chart feature
    rich - For Terminal feature
History:
    19/06/2021(v0.0.0.1) - First made the library and updated it
    20/06/2021(v0.1) - Added many features
    21/06/2021(v0.1.9) - Bug fixes
    26/06/2021(v0.2.0) - Made Improvements and added new features
    27/06/2021(v0.2.6) - Bug Fixes and update and made the 'Studio' class
    03/07/2021(v0.4.5) - Added many functions and made the 'Project' class
    04/07/2021(v0.5.0) - Update
    05/07/2021(v0.5.1) - Updated the messages function
    06/07/2021(v0.6.0) - Updated CloudConnection
    08/07/2021(v0.7.5) - Updated CloudConnection
    10/07/2021(v0.7.5) - Updated CloudConnection, made the Forum class and added DocString
    13/07/2021(v0.9.7) - Added DocString
    14/07/2021(v0.9.0) - Bug Fixes
    15/07/2021(v1.0) - First Release
    18/07/2021(V1.1) - Made the 'studio.get_projects()'
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
    16/03/2022(v2.5) - Fixed login and added cookie login feature
    26/03/2022(v2.6) - Added some more APIs
    27/03/2022(v2.6.3) - Added the Scratch Terminal Feature
    28/03/2022(v2.7.5) - Updated the Scratch Terminal Feature and added the Chart Feature
    29/03/2022(v2.8) - Updated the Charts Feature
    16/04/2022(v3.0.1) - Bug fixes and improvements
    30/04/2022(v3.0.5) - Code fix
    01/05/2022(v3.0.8) - Code fix and new features
    07/05/2022(v3.0.9) - Code fix
    12/05/2022(v3.1) - Updated the CloudConnection Class
    04/06/2022(v3.2) - Updated the ScratchConnect, CloudStorage, etc. Class
    05/06/2022(v3.3) - Updated the CloudEvents Class, etc
    08/06/2022(v3.3.5) - Added colored messages, etc
    11/06/2022(v3.4) - Updated and made the CloudStorage Feature faster
    05/08/2022(v3.4.1) - Planed and added some features of Online IDE login
    06/08/2022(v3.4.2) - Added the OnlineIDE feature to all the Scratch API based classes
    08/08/2022(v3.4.5) - Planned the Cloud Requests feature
    09/08/2022(v3.5) - Added some features to the Cloud Requests Class
    13/08/2022(v3.5.1) - Added some methods to the TurbowarpCloudConnection and CloudRequests classes and updated them
    14/08/2022(v3.5.6) - Updated the Cloud Requests Class
    15/08/2022(v3.6.0) - Updated the Cloud Requests Class
    16/08/2022(v3.6.0) - Updated the Cloud Requests Class and added some logs to the class
    20/08/2022(v3.7) - Added more logs to the Requests Class
    21/08/2022(v3.8) - Made the scImage Class
    27/08/2022(v3.9) - Reduced the size of encoded Image
    30/08/2022(v3.9.5) - Bug fixes and Improvements
    24/09/2022(v3.9.6) - Bug fixes and Improvements
    25/09/2022(v3.9.7) - Bug fixes and Improvements
    26/09/2022(v3.9.9) - Fixed many bugs in scCloudRequests
    14/12/2022(v4.0.0) - Fixed the arguments bug in the Cloud Requests feature
    15/12/2000(v4.0.0) - Bug fixes and improvements in the Cloud Requests feature
Credits:
    All code by Siddhesh Chavan. Thanks to other contributors.
Information:
    Module made by:- Siddhesh Chavan
    Age:- 15 (as of 2022)
    Email:- siddheshchavan2020@gmail.com
    YouTube Channel:- Siddhesh Chavan (Link: https://www.youtube.com/channel/UCWcSxfT-SbqAktvGAsrtadQ)
    Scratch Account:- @Sid72020123 (Link: https://scratch.mit.edu/users/Sid72020123/)
    My self-made Website: https://Sid72020123.github.io/
"""

print_name = "ScratchConnect"
print(f"[1m[33m{print_name}[32m[3m v{__version__}[37m -[36m {__documentation__}[0m")

from scratchconnect.ScratchConnect import ScratchConnect
from scratchconnect import Exceptions
