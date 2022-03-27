# scratchconnect v2.6

Python Library to connect Scratch API and much more.

This library can show the statistics of Users, Projects, Studios, Forums and also connect and set cloud variables of a
project!

**This library needs a Scratch account. Visit the Scratch Website: [https://scratch.mit.edu/](https://scratch.mit.edu/)
You also need to have the Python programming language installed on your computer.**

**You need basic knowledge of Python. Using this library without the knowledge can be risky.**

![https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![PyPI Latest Release](https://img.shields.io/pypi/v/scratchconnect.svg)](https://pypi.org/project/scratchconnect/)
[![Package Status](https://img.shields.io/pypi/status/scratchconnect.svg)](https://pypi.org/project/scratchconnect/)
[![Downloads](https://static.pepy.tech/personalized-badge/scratchconnect?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/scratchconnect)

[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Sid72020123/scratchconnect.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Sid72020123/scratchconnect/context:python)

### Installation

To install this library, just type ```pip install scratchconnect``` in the terminal (Command Prompt)

**OR**

Run this Python program

```python
import os

os.system('pip install scratchconnect')
```

**If you still have troubles while installing then go
to [this link](https://packaging.python.org/tutorials/installing-packages/)**

### Documentation

Documentation coming soon...

### Data Credits:

These are the people who made the APIs so that this library can take data:

* [Scratch API](https://github.com/LLK/scratch-rest-api) by the Scratch Team
* [Scratch DB](https://scratchdb.lefty.one/) by [@DatOneLefty](https://scratch.mit.edu/users/DatOneLefty/) on Scratch
* [Scratch Comments API](https://github.com/Sid72020123/Scratch-Comments-API)
  by  [@Sid72020123](https://scratch.mit.edu/users/Sid72020123/) on Scratch
* [Simple Forum API](https://github.com/Sid72020123/Scratch-Forum)
  by [@Sid72020123](https://scratch.mit.edu/users/Sid72020123/) on Scratch

```
I thank all these people.
- Owner (Sid72020123)
```

### Creating a Simple Connection:

Following is a simple program to make a simple connection:

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
```

It will give an error if the `username` or `password` is invalid.

### More Uses:

##### Note: The below code can be only used by the logged in Scratcher. To get the stats of other users see the User Connection Documentation

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
user.id()  # Returns the ID of the user
user.thumbnail_url()  # Returns the thumbnail URL of a user
user.messages_count()  # Returns the messages count of the user
user.messages(all=False, limit=20, offset=0, filter="all")  # Returns the messages
user.work()  # Returns the 'What I am working on' of a Scratch profile
user.bio()  # Returns the 'About me' of a Scratch profile
user.status()  # Returns the status(Scratcher or New Scratcher) of a Scratch profile
user.joined_date()  # Returns the joined date of a Scratch profile
user.country()  # Returns the country of a Scratch profile
user.featured_data()  # Returns the featured project data of the Scratch profile
user.projects()  # Returns the list of shared projects of a user
user.followers_count()  # Returns the follower count of a user
user.following_count()  # Returns the following count of a user
user.total_views()  # Returns the total views count of all the shared projects of a user
user.total_loves_count()  # Returns the total loves count of all the shared projects of a user
user.total_favourites_count()  # Returns the total favourites count of all the shared projects of a user
user.following()  # Returns the list of the user following
user.followers()  # Returns the list of the user followers
user.favourites()  # Returns the list of the user favourites
user.toggle_commenting()  # Toggle the commenting of the profile
user.follow_user(username="Sid72020123")  # Follow a user
user.unfollow_user(username="Sid72020123")  # UnFollow a user
user.set_bio(content="Hi!")  # Set the bio or 'About Me' of the profile
user.set_work(content="Hi!")  # Set the status or 'What I am Working On' of the profile
user.all_data()  # Returns all the data of the user
user.site_health()  # Returns the health of the Scratch Website.
user.site_news()  # Returns the news of the Scratch Website.
user.site_front_page_projects()  # Returns the front page projects of the Scratch Website.
user.explore_projects(mode="trending", query="*")  # Explore the projects
user.explore_studios(mode="trending", query="*")  # Explore the studios
user.search_projects(mode="trending", search="*")  # Search the projects
user.search_studios(mode="trending", search="*")  # Search the studios
user.set_featured_project(project_id="1", label='featured_project')  # Set the 'Featured Project' of a Scratch Profile
user.user_follower_history()  # Return the follower history of the user
user.comments(limit=5, page=1)  # Get comments of the profile of the user
user.ocular_data()  # Returns the ocular data of the user
user.search_forum(q="Hi!", order="relevance", page=0)  # Search the forum
##########################################################################
# IMPORTANT NOTE: To always get the updated data use the update_data() function
##########################################################################
user.update_data()  # Update the data
```

### Connect a Scratch User:

To connect a Scratch User use the `connect_user()` function. Use the following program to connect a Scratch User:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")
user = login.connect_user(username="Sid72020123")
user.id()  # Returns the ID of the user
user.thumbnail_url()  # Returns the thumbnail URL of a user
user.messages_count()  # Returns the messages count of the user
user.work()  # Returns the 'What I am working on' of a Scratch profile
user.bio()  # Returns the 'About me' of a Scratch profile
user.status()  # Returns the status(Scratcher or New Scratcher) of a Scratch profile
user.joined_date()  # Returns the joined date of a Scratch profile
user.country()  # Returns the country of a Scratch profile
user.featured_data()  # Returns the featured project data of the Scratch profile
user.projects()  # Returns the list of shared projects of a user
user.followers_count()  # Returns the follower count of a user
user.following_count()  # Returns the following count of a user
user.total_views_count()  # Returns the total views count of all the shared projects of a user
user.total_loves_count()  # Returns the total loves count of all the shared projects of a user
user.total_favourites_count()  # Returns the total favourites count of all the shared projects of a user
user.following()  # Returns the list of the user following
user.followers()  # Returns the list of the user followers
user.favourites()  # Returns the list of the user favourites
user.user_follower_history()  # Return the follower history of the user
user.post_comment(content="Hi!")  # Post a comment on the user's profile
user.report(field="")  # Report a user
user.reply_comment(content="Hi!", comment_id=1)  # Reply a comment
user.all_data()  # Returns all the data of the user
user.comments(limit=5, page=1)  # Get comments of the profile of the user
user.ocular_data()  # Returns the ocular data of the user
##########################################################################
# IMPORTANT NOTE: To always get the updated data use the update_data() function
##########################################################################
user.update_data()  # Update the data
```

### Connect a Scratch Studio:

To connect a Scratch Studio use the `connect_studio()` function. Use the following program to connect a Scratch Studio:

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
studio = user.connect_studio(studio_id=1)
studio.id()  # Returns the studio ID
studio.title()  # Returns the studio title
studio.host_id()  # Returns the studio owner/host ID
studio.description()  # Returns the studio description
studio.visibility()  # Returns the studio visibility
studio.is_public()  # Returns whether a studio is public
studio.is_open_to_all()  # Returns whether a studio is open to all
studio.are_comments_allowed()  # Returns whether a studio has comments allowed
studio.history()  # Returns the history of the studio
studio.stats()  # Returns the stats of the studio
studio.thumbnail_url()  # Returns the thumbnail URL of the studio
studio.add_project(project_id=1)  # Add a project to a studio
studio.remove_project(project_id=1)  # Remove a project from a studio
studio.open_to_public()  # Open the studio to public
studio.close_to_public()  # Close the studio to public
studio.follow_studio()  # Follow the studio
studio.unfollow_studio()  # UnFollow the studio
studio.toggle_commenting()  # Toggle the commenting of the studio
studio.post_comment(content="Hi!")  # Post comment in the studio
studio.reply_comment(content="Hi!", comment_id=1)  # Reply a comment in a studio
studio.delete_comment()  # Delete comment in the studio
studio.report_comment(comment_id=1)  # Report comment in the studio
studio.invite_curator(username="Sid72020123")  # Invite a user to the studio
studio.accept_curator()  # Accept the curator invitation in a studio
studio.promote_curator(username="Sid72020123")  # Promote a user in the studio
studio.set_description(content="Hi!")  # Set the description of a Studio
studio.set_title(content="Hi!")  # Set the title of a Studio
studio.projects(all=False, limit=40, offset=0)  # Get the projects of the studio
studio.comments(all=False, limit=40, offset=0)  # Get the comments of the studio
studio.curators(all=False, limit=40, offset=0)  # Get the curators of the studio
studio.managers(all=False, limit=40, offset=0)  # Get the managers of the studio
studio.activity(all=False, limit=40, offset=0)  # Get the activity of the studio
##########################################################################
# IMPORTANT NOTE: To always get the updated data use the update_data() function
##########################################################################
studio.update_data()  # Update the data
```

### Connect a Scratch Project:

To connect a Scratch Project use the `connect_project()` function. Use the following program to connect a Scratch
Project:

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
project = user.connect_project(project_id=1)  # Connect a project.
project.author()  # Returns the author of the project
project.title()  # Returns the title of the project
project.notes()  # Returns the notes(Notes or Credits) of the project
project.instruction()  # Returns the instructions of the project
project.are_comments_allowed()  # Returns whether the comments are allowed in a project
project.stats()  # Returns the stats of a project
project.history()  # Returns the history of a project
project.remix_data()  # Returns the remix data of a project
project.visibility()  # Returns whether the project is visible
project.is_public()  # Returns whether the project is public
project.is_published()  # Returns whether the project is published
project.thumbnail_url()  # Returns the thumbnail url of a project
project.assets_info()  # Returns the Assets info of a project
project.scripts()  # Returns the scripts of a project
project.love()  # Love a project
project.unlove()  # UnLove a project
project.favourite()  # Favourite a project
project.unfavourite()  # UnFavourite a project
project.comments(all=False, limit=40, offset=0, comment_id=None)  # Returns the list of comments of a project
project.remixes(all=False, limit=20, offset=0)  # Returns the list of remixes of a project
project.post_comment(content="Hi!")  # Post a comment
project.reply_comment(content="Hi!", comment_id=1)  # Reply a comment
project.toggle_commenting()  # Toggle the commenting of a project
project.turn_on_commenting()  # Turn On the commenting of a project
project.turn_off_commenting()  # Turn Off the commenting of a project
project.report(category="", reason="")  # Report a project
project.unshare()  # Unshare a project
project.view()  # Just view a project
project.set_thumbnail(file="")  # Set the thumbnail of a project
project.delete_comment(comment_id=1)  # Delete a comment
project.report_comment(comment_id=1)  # Report a comment
project.reply_comment(comment_id=1, content="Hi!")  # Reply a comment
project.set_title()  # Set the title of the project
project.set_description()  # Set the description of the project
project.set_instruction()  # Set the instruction of the project
##########################################################################
# IMPORTANT NOTE: To always get the updated data use the update_data() function
##########################################################################
project.update_data()  # Update the data
```

#### Want to access and set the cloud variables of an unshared project?

Use the Following Code:

**Note: By accessing an unshared project, some data may not be accessible to this library so some data might not appear.
You can get the scripts and connect cloud variables of an unshared project.**

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
project = user.connect_project(project_id=1,
                               access_unshared=True)  # Use the 'access_unshared' parameter to access the unshared project.
```

### Connect Cloud Variables of a Scratch Project:

To connect the cloud variables of a Scratch Project use the `connect_cloud_variables()` function. Use the following
program to connect the cloud variables of a Scratch Project:

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
project = user.connect_project(project_id=1)
variables = project.connect_cloud_variables()
variables.get_variable_data(limit=100, offset=0)  # Returns the cloud variable data
variables.get_cloud_variable_value(variable_name="Name", limit=100)  # Returns the cloud variable value
# Program to set cloud variables:
set = variables.set_cloud_variable(variable_name="Name", value=123)  # Set a Cloud Variable
if set:
    print("Cloud Variable Updated!")
```

### Connect Cloud Variables of Turbowarp:

To connect the cloud variables of a Turbowarp Project use the `connect_turbowarp_cloud()` function. Use the following
program to connect the cloud variables of a Turbowarp Project:

**Note: Turbowarp doesn't provide any features to get the data, etc. so you can't do some actions with Turbowarp as in
Scratch**

**Note: Use the ```acccess_unshared=True``` parameter of the ```connect_project()``` function to connect the Turbowarp
Project even if it is unshared on Scratch!**

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
project = user.connect_project(project_id=1)  # Connect a Project
tw_cloud = project.connect_turbowarp_cloud(
    username="Username")  # Connect the Turbowarp cloud with an optional parameter to change the username!

tw_cloud.set_cloud_variable(variable_name="Name", value=0)  # Set a Turbowarp variable

tw_cloud.get_variable_data()  # Get the data of the previous value of the variable. NOT Current
```

### Error with Turbowarp Cloud?

Sometimes there mat be error with the Turbowarp Cloud. Some Basic Errors are:

**1. I can't change the Cloud Variable Value**

If you can't change the Turbowarp Cloud Variable value using scratchconnect then first check if your code is correct. If
the problem still exists try with this
URL: ```https://turbowarp.org/<project ID>?cloud_host=wss://clouddata.turbowarp.org```. Replace the ```project ID```
with your project ID.

### Encoding/Decoding Cloud Variables:

#### In Scratch

ScratchConnect v2.0+ has some good features to encode/decode a cloud variable! See some examples below:

**ScratchConnect has a case-sensitive encoding/decoding system. For example both 'A' and 'a' are encoded/decoded
differently!**

Go to [this link](https://scratch.mit.edu/projects/578255313/) for the Scratch version of Encoder/Decoder

##### Encoding/Decoding a string:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")
project = login.connect_project(1)  # Connect the project

variables = project.connect_cloud_variables()  # Connect the project's cloud variables

encoded_string = variables.encode("Hi! This is a text!")  # Encode a string

variables.set_cloud_variable(variable_name='Name', value=encoded_string)
variable_value = variables.get_cloud_variable_value(variable_name='Name')[0]  # Get the variable value

decoded_string = variables.decode(variable_value)  # Decode a string

print("Encoded: ", encoded_string)  # Print the results to check
print("Decoded: ", decoded_string)  # Print the results to check
```

##### Encoding/Decoding a list:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")
project = login.connect_project(1)  # Connect the project

variables = project.connect_cloud_variables()  # Connect the project's cloud variables

data = ['A', 'B', 'C']
encoded_string = variables.encode_list(data)  # Encode a list

variables.set_cloud_variable(variable_name='Name', value=encoded_string)
variable_value = variables.get_cloud_variable_value(variable_name='Name')[0]  # Get the variable value

decoded_string = variables.decode_list(variable_value)  # Decode a list

print("Encoded: ", encoded_string)  # Print the results to check
print("Decoded: ", decoded_string)  # Print the results to check
```

#### In Turbowarp

To encode/decode a string/list in Turbowarp, the syntax is same as to encode/decode in Scratch. See above

### Connect a Scratch Forum:

To connect a Scratch Forum use the `connect_forum_topic()` function. Use the following program to connect a Scratch
Forum:

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
forum = user.connect_forum_topic(forum_id=1)
forum.id()  # Returns the id of the forum
forum.title()  # Returns the title of the forum
forum.category()  # Returns the category of the forum
forum.closed()  # Returns whether the forum is closed or not
forum.deleted()  # Returns whether the forum is deleted or not
forum.time()  # Returns the activity of the forum
forum.post_count()  # Returns the total post count of the forum
forum.follow()  # Follow a Forum
forum.unfollow()  # Unfollow a Forum
forum.posts(page=1)  # Get the post in Forum Topic of a specified page. Images and some other stuff will not appear!
forum.ocular_reactions(post_id=123)  # Get the ocular reactions of the post
forum.topic_post_history(usernames="total", segment="1", range="30")  # Get the post history of the topic
##########################################################################
# IMPORTANT NOTE: To always get the updated data use the update_data() function
##########################################################################
forum.update_data()  # Update the data
```

### Cloud Events

**This new feature was suggested by [@Ankit_Anmol](https://scratch.mit.edu/users/Ankit_Anmol/) on Scratch**
If you want to handle various Cloud Events on Scratch, use the following code:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")
project = login.connect_project(1)  # Connect the project

variables = project.connect_cloud_variables()  # Connect the project's cloud variables

event = variables.start_event(
    update_time=1)  # Start a cloud event loop to check events. Use the 'update_time' parameter to wait for that number of seconds and then update the data.


@variables.event.on('change')
def do_something(**data):
    print(data)  # Will print variable data of the event in dict format. You can access individual members too! Example:
    print(data['user'])  # The user who changes the value
    print(data['action'])  # The action with the variable
    print(data['variable_name'])  # The name of the variable changed, created, etc.
    print(data['value'])  # The value of the variable
    print(data['timestamp'])  # The timestamp
```

**Want to check if only a variable's value if updated? See this example code:**

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")
project = login.connect_project(1)  # Connect the project

variables = project.connect_cloud_variables()
event = variables.start_event(update_time=1)  # Start Event with the required time.


@variables.event.on('change')
def do_something(**data):
    event_type = data['action']  # Will contain variable action of the event.
    if event_type == 'set_var':
        # Do something when a value is changed...
        print(data['variable_name'], data['value'])  # Just print the data name and value.
```

### Cloud Storage (beta)

This is a special feature in ScratchConnect which is used to make a cloud storage system. Some features are:

* Create a variable
* Set a variable
* Get a variable
* Delete a variable
* Delete all variables
* Wait for a given time
* Simple Syntax

**Note: This feature is still in development and may cause errors! Creating/Deleting variables is fast but
Getting/Setting them is a little slow.**

**First, you need to put a sprite in your project. Go to [this link](https://scratch.mit.edu/projects/606881698/) and
click 'see inside'. There will be all the instructions.**

To create a cloud storage in ScratchConnect use the code:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")
project = login.connect_project(1)  # Connect the project

cloud_storage = project.create_cloud_storage(file_name="data", rewrite_file=False, edit_access=[
    'Sid72020123'])  # Create a cloud storage. It will create a file in the specified location. Then there is 'edit_access' list which contains the users which have permission to edit(actually create and delete) the variables. Use the 'rewrite_file' argument if you want the file to be rw written again each time you write the program!

cloud_storage.start_cloud_loop(update_time=1,
                               print_requests=True)  # Start the Cloud Storage. Use the 'update_time' to wait for the specified time. Use the 'print_requests' to print the request info in the console/output screen.
```

### Cookie Login

Sometimes, the Scratch API blocks the login from online IDEs like Replit, etc. To overcome the issue, ScratchConnect
v2.5 or above has a feature to login directly with cookie. Example:

```python
import scratchconnect

scratch_cookie = {
    "Username": "USERNAME",
    "SessionID": "SESSIONID",
    "CSRFToken": "CSRFTOKEN"
}  # set the cookie dictionary

login = scratchconnect.ScratchConnect(cookie=scratch_cookie)  # Login with cookie
```

**Note: While running the above code, ScratchConnect will give a warning that some features might not work if the cookie
values are wrong. It's not an ERROR, it's a WARNING**

#### Advanced

In case the login from username and password fails, ScratchConnect also has a feature to login with a cookie when the
login with username and password fails! You just have to pass the username and password value and also the cookie in the
ScratchConnect class. Also, you need to set the `auto_cookie_login` variable to `True`. Example Code:

```python
import scratchconnect

scratch_cookie = {
    "Username": "USERNAME",
    "SessionID": "SESSIONID",
    "CSRFToken": "CSRFTOKEN"
}  # set the cookie dictionary

login = scratchconnect.ScratchConnect(username="USERNAME", password="PASSWORD",
                                      cookie=scratch_cookie,
                                      auto_cookie_login=True)  # Login with cookie and enable the auto_cookie_login
```

### Projects made using ScratchConnect

To see the projects made using ScratchConnect, go to the
official [ScratchConnect Projects Studio](https://scratch.mit.edu/studios/30427944/)

### Bug Reporting:

All Bugs to be reported on my [Scratch Profile](https://scratch.mit.edu/users/Sid72020123/)
or [Github](https://github.com/Sid72020123/scratchconnect/issues)

### Change Log:

* 19/06/2021(v0.0.0.1) - First made the library and updated it.
* 20/06/2021(v0.1) - Added many features.
* 21/06/2021(v0.1.9) - Bug fixes.
* 26/06/2021(v0.2.0) - Made Improvements and added new features.
* 27/06/2021(v0.2.6) - Bug Fixes and update and made the 'Studio' class.
* 03/07/2021(v0.4.5) - Added many functions and made the 'Project' class.
* 04/07/2021(v0.5.0) - Update.
* 05/07/2021(v0.5.1) - Updated the messages function.
* 06/07/2021(v0.6.0) - Updated CloudConnection.
* 08/07/2021(v0.7.5) - Updated CloudConnection.
* 10/07/2021(v0.7.5) - Updated CloudConnection, made the Forum class and added DocString.
* 13/07/2021(v0.9.7) - Added DocString.
* 14/07/2021(v0.9.0) - Bug Fixes.
* 15/07/2021(v1.0) - First Release!
* 18/07/2021(V1.1) - Made the 'studio.get_projects()'.
* 19/07/2021(v1.2) - Made the get comments, curators, managers of the studio
* 13/08/2021(v1.3) - Added the get comments function
* 14/08/2021(v1.4) - Updated the get messages function
* 17/08/2021(v1.5) - Made some bug fixes
* 18/09/2021(v1.7) - Made the ScratchConnect and User Classes fast and Improved methods
* 19/09/2021(v1.8) - Made the Studio Class Faster and Improved methods
* 25/09/2021(v1.8.5) - Updated the Project and User classes
* 02/10/2021(v2.0) - Updated the Cloud and Forum Class
* 10/10/2021(v2.0.1) - Fixed some cloud stuff
* 11/10/2021(v2.1) - Added some features to Forum Class
* 24/10/2021(v2.1.1) - Started making the scStorage Class
* 29/10/2021(v2.1.1.1) - Fixed set_bio() and set_work() and updated the scDataBase
* 30/10/2021(v2.2.5) - Updated the scStorage
* 31/10/2021(v2.2.7) - Updated the scStorage
* 25/11/2021(v2.3) - Updated the scStorage and CloudConnection
* 13/12/2021(v2.3.5) - Started making the TurbowarpCloudConnection feature and added some methods to it
* 14/12/2021(v2.4) - Updated and fixed mistakes in docs
* 09/01/2022(v2.4.1) - Code Fixes
* 25/01/2022(v2.4.2) - Added new Comment API
* 16/03/2022(v2.5) - Fixed login and added cookie login feature
* 26/03/2022(v2.6) - Added some more APIs

### Credits:

**This library is made by [@Sid72020123](https://scratch.mit.edu/users/Sid72020123/) on Scratch. And thanks to all
contributors.**

### Contributors:

***The names of persons below are their Scratch Usernames.***

| **Person**      | **Role**      | **Work**                                                       |
|-----------------|---------------|----------------------------------------------------------------|
| **Sid72020123** | *Owner*       | Made the library and most of its features                      |
| **Ankit_Anmol** | *Contributor* | Fixed some things in the documentation and added some features |
| **Chiroyce**    | *Contributor* | Added some features and cleaned up some code                   |
| **god286**      | *Contributor* | Fixed mistakes in the documentation                            |

*If I'm missing some people and their work in the contributors table, please contact Sid72020123 on Scratch*

