# ScratchConnect v4.5.2

Python Library to connect Scratch API and much more.

This library can show the statistics of Users, Projects, Studios, Forums and also connect and set cloud variables of a
project!

**This library needs a Scratch account. Visit the Scratch Website: [https://scratch.mit.edu/](https://scratch.mit.edu/)
You also need to have the Python programming language installed on your computer.**

**You need basic knowledge of Python. Using this library without the knowledge can be risky.**

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue&color=black)

![PyPI](https://img.shields.io/pypi/v/scratchconnect)
[![Package Status](https://img.shields.io/pypi/status/scratchconnect)](https://pypi.org/project/scratchconnect/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/scratchconnect)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/sid72020123/scratchconnect)

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

Documentation is taking a bit longer to make. It will be ready soon...

### Data Credits:

These are the people who made the APIs so that this library can take data:

* [Scratch API](https://github.com/LLK/scratch-rest-api) by the Scratch Team
* [Scratch DB](https://scratchdb.lefty.one/) by [@DatOneLefty](https://scratch.mit.edu/users/DatOneLefty/) on Scratch
* [Scratch Comments API](https://github.com/Sid72020123/Scratch-Comments-API)
  by  [@Sid72020123](https://scratch.mit.edu/users/Sid72020123/) on Scratch
* [Simple Forum API](https://github.com/Sid72020123/Scratch-Forum)
  by [@Sid72020123](https://scratch.mit.edu/users/Sid72020123/) on Scratch
* [Ocular API](https://ocular.jeffalo.net/) by [@Jeffalo](https://scratch.mit.edu/users/Jeffalo/) on Scratch
* [Aviate API](https://aviateapp.eu.org/) by [@NFlex23](https://scratch.mit.edu/users/NFlex23/) on Scratch

```
I thank all these people.
- Owner (Sid72020123)
```

### Creating a Simple Connection:

Following is a simple program to make a simple connection:

**Note: Don't put the username and password as it is when you host or share the code with others. While hosting, you can
use environment variables and while sharing, you can remove the username and password values. This will help in keeping
the password and other important things secured.**

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
```

It will give an error if the `username` or `password` is invalid.

### More Uses:

##### Note: Some of the functions below can be only used by the logged in Scratcher. To get the stats of other users see the User Connection Documentation

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
user.id()  # Returns the ID of the user
user.thumbnail_url()  # Returns the thumbnail URL of a user
user.messages_count()  # Returns the messages count of the user
user.messages(all=False, limit=20, offset=0, filter="all")  # Returns the messages
user.clear_messages()  # Clear your messages
user.my_stuff_projects(order="all", page=1, sort_by="")  # Get/Sort mystuff projects
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
user.aviate_data(code=False)  # Returns the Aviate Status of the user
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
user.aviate_data(code=False)  # Returns the Aviate Status of the user
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
studio.all_data()  # Returns all the data of a Scratch Studio
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
project.all_data()  # Returns all the data of a Scratch Project
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

Sometimes there may be an error with the Turbowarp Cloud. Some Basic Errors are:

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

If you want to handle various Cloud Events on Scratch, use the following code:

#### In Scratch:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")

project = login.connect_project(1)  # Connect the project

cloud = project.connect_cloud_variables()  # Connect the project's cloud

event = cloud.create_cloud_event()  # Create a cloud event


@event.on("connect")
def connect():
    print("Connected Cloud!")


@event.on("set")
def set(data):
    print("SET: ", data)


@event.on("create")
def create(data):
    print("CREATE: ", data)


@event.on("delete")
def delete(data):
    print("DELETE: ", data)


@event.on("disconnect")
def disconnect():
    print("Disconnected from Cloud!")


event.start(update_time=1)  # Start the event with update time

# To Stop a Cloud Event, use the event.stop() function
```

#### In Turbowarp:

Use the same method as in Scratch but this time connect the cloud of a project on Turbowarp

### Cloud Storage

**IMPORTANT NOTE: This feature is going to be discontinued in ScratchConect v5.0! Please use the new alternative feature: Cloud Requests.**

This is a special feature in ScratchConnect which is used to make a cloud storage system. Some features are:

* Create a variable
* Set a variable
* Get a variable
* Delete a variable
* Delete all variables
* Wait for a given time
* Simple Syntax

**Note: Maximum of 1024 characters can be set as a value to a variable. You can create any number of variables!**

**First, you need to put a sprite in your project. Go to [this link](https://scratch.mit.edu/projects/606881698/) and
click 'see inside'. There will be all the instructions.**

To create a cloud storage in ScratchConnect use the code:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")
project = login.connect_project(1)  # Connect the project

cloud_storage = project.create_cloud_storage(file_name="data", rewrite_file=False, edit_access=[
    'Sid72020123'],
                                             all_access=False)  # Create a cloud storage. It will create a file in the specified location. Then there is 'edit_access' list which contains the users which have permission to edit(actually create and delete) the variables. Use the 'rewrite_file' argument if you want the file to be re-written again each time you write the program! You can set the 'all_access' to True if you want to give all the access to all users!

cloud_storage.start_cloud_loop(update_time=1,
                               print_requests=True)  # Start the Cloud Storage. Use the 'update_time' to wait for the specified time. Use the 'print_requests' to print the request info in the console/output screen.
```

### Cookie Login

Sometimes, the Scratch API blocks the login from online IDEs like Replit, etc. To overcome the issue, ScratchConnect
v2.5 or above has a feature to login directly with cookie. Example:

**How to get a cookie?**
You can get your cookie values by logging in with ScratchConnect locally on your computer and use the login object as ```print(login.session_id)``` to get the required cookie value. Copy the value and store it in environment variable if you are using an online IDE like Replit!

**Note: Keep this values secured and use environment variables wherever necessary.**

```python
import scratchconnect

scratch_cookie = {
    "Username": "Your username",
    "SessionID": "Your SessionID",
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
    "Username": "Your username",
    "SessionID": "Your SessionID",
}  # set the cookie dictionary

login = scratchconnect.ScratchConnect(username="USERNAME", password="PASSWORD",
                                      cookie=scratch_cookie,
                                      auto_cookie_login=True)  # Login with cookie and enable the auto_cookie_login
```

### Using ScratchConnect without login

With ScratchConnect v3.1+, you can use it without login! Example code:

```python
import scratchconnect

user = scratchconnect.ScratchConnect()  # Leave all the values empty to use this library without login!
```

**Note: If you login without a username and password, some features such as setting cloud variables, etc. may not work.
It will give you a warning when you use this library without login!**

### Terminal

ScratchConnect v3.0+ has a feature called "Terminal" in which a user can get the data of Scratch User, Studio and
Project in the Python console.

To use this feature, you need to install additional dependencies required, by
typing ```pip install scratchconnect[terminal]``` in the command prompt/terminal. Then, see the example code:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")

terminal = login.create_new_terminal()  # Create a new Terminal object
terminal.start()  # Start the main terminal program
```

You can use many features in it. Just enter ```help``` to see the list of commands after the terminal starts.

### Charts

ScratchConnect v3.0+ has a feature called "Chart" in which a user can get the data of Scratch User, Studio and Project
in graphical format.

**Note: This feature uses the library ```pyhtmlchart``` to create graphs. Any other library can be used in later
versions.**

To use this feature, you need to install additional dependencies required, by
typing ```pip install scratchconnect[chart]``` in the command prompt/terminal

#### User Comparison Chart:

See the example code:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")

chart = login.create_new_chart()  # Create a Chart object

user_chart = chart.user_stats_chart(
    usernames=["griffpatch", "Will_Wam", "ScratchCat"])  # Create users stats comparison chart

user_table = chart.user_stats_table(
    usernames=["griffpatch", "Will_Wam", "ScratchCat"])  # Create users stats comparison table

user_chart.open()  # Open User chart
user_table.open()  # Open User table
```

To include only some required data in a chart or table, use the ```include_data``` parameter of the chart or table
function and pass the value as list to get the required data.
Example: ```['Messages Count', 'Follower Count', 'Following Count']```

You can also use any one or more options from the following list:

```python
['Username', 'Messages Count', 'Follower Count', 'Following Count', 'Total Loves',
 'Total Favourites', 'Total Projects Count']
```

#### Studio Comparison Chart:

See the example code:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")

chart = login.create_new_chart()  # Create a Chart object

studio_chart = chart.studio_stats_chart(
    studio_ids=[100, 101, 102])  # Create studio stats comparison chart

studio_table = chart.studio_stats_table(
    studio_ids=[100, 101, 102])  # Create studio stats comparison table

studio_chart.open()  # Open Studio chart
studio_table.open()  # Open Studio table
```

To include only some required data in a chart or table, use the ```include_data``` parameter of the chart or table
function and pass the value as list to get the required data.
Example: ```['Comments Count', 'Followers Count', 'Managers Count']```

You can also use any one or more options from the following list:

```python
['Studio ID', 'Comments Count', 'Followers Count', 'Managers Count', 'Projects Count']
```

#### Project Comparison Chart:

See the example code:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")

chart = login.create_new_chart()  # Create a Chart object

project_chart = chart.project_stats_chart(
    project_ids=[104, 105, 106])  # Create project stats comparison chart

project_table = chart.project_stats_table(
    project_ids=[104, 105, 106])  # Create project stats comparison table

project_chart.open()  # Open Project chart
project_table.open()  # Open Project table
```

To include only some required data in a chart or table, use the ```include_data``` parameter of the chart or table
function and pass the value as list to get the required data. Example: ```['Views', 'Loves', 'Favourites']```

You can also use any one or more options from the following list:

```python
['Project ID', 'Views', 'Loves', 'Favourites', 'Remixes', 'Version', 'Costumes', 'Blocks',
 'Variables', 'Assets']
```

#### User Follower History Chart:

See the example code:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")

chart = login.create_new_chart()  # Create a Chart object

c = chart.user_followers_history_chart(username="griffpatch")  # Followers History Chart

t = chart.user_followers_history_table(username="griffpatch")  # Followers History Table

c.open()  # Open chart
t.open()  # Open table
```

### Using ScratchConnect in online IDEs like Replit

Using the ScratchConnect version ```4.0.0+```, you can use this library even on some online IDEs like Replit!

But to keep your profile data safe, this supports only ```GET``` requests and no cookie headers are passed to the proxy (which this feature uses).
You cannot perform any actions other than ```GET```, i.e., follow a user, post a comment, etc.

But cloud variables work as it is a websocket connection.

**Remember to use environment variables to store your session ID if you are using this on an online IDE like Replit...**

To use ScratchConnect in online IDEs like Replit, you need to get your session ID (see Cookie-Login section above) and the code like:
```python
import scratchconnect

session_id = "<your session id here>"
cookie = {
   "Username": "<your username>",
   "SessionID": session_id
}

login = scratchconnect.ScratchConnect(online_ide_cookie=cookie) # Pass the cookie variable as a parameter to the ScratchConnect class

# Your code here...
```

### Cloud Requests

This feature was first released in version ```4.0.0``` of the ScratchConnect Python Library.
Using this, you will be able to send any amount of data to-and-from your Python program and any Scratch Project.

The docs to use this feature are [here](https://github.com/Sid72020123/scratchconnect/blob/main/CLOUD_REQUESTS.md)

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
* 27/03/2022(v2.6.3) - Added the Scratch Terminal Feature
* 28/03/2022(v2.7.5) - Updated the Scratch Terminal Feature and added the Chart Feature
* 29/03/2022(v2.8) - Updated the Charts Feature
* 16/04/2022(v3.0) - Bug fixes and improvements
* 30/04/2022(v3.0.5) - Code fix
* 01/05/2022(v3.0.8) - Code fix and new features
* 07/05/2022(v3.0.9) - Code fix
* 12/05/2022(v3.1) - Updated the CloudConnection Class
* 04/06/2022(v3.2) - Updated the ScratchConnect, CloudStorage, etc. Class
* 05/06/2022(v3.3) - Updated the CloudEvents Class, etc
* 08/06/2022(v3.3.5) - Added colored messages, etc
* 11/06/2022(v3.4) - Updated and made the CloudStorage Feature faster
* 05/08/2022(v3.4.1) - Planed and added some features of Online IDE login
* 06/08/2022(v3.4.2) - Added the OnlineIDE feature to all the Scratch API based classes
* 08/08/2022(v3.4.5) - Planned the Cloud Requests feature
* 09/08/2022(v3.5) - Added some features to the Cloud Requests Class
* 13/08/2022(v3.5.1) - Added some methods to the TurbowarpCloudConnection and CloudRequests classes and updated them
* 14/08/2022(v3.5.6) - Updated the Cloud Requests Class
* 15/08/2022(v3.6.0) - Updated the Cloud Requests Class
* 16/08/2022(v3.6.0) - Updated the Cloud Requests Class and added some logs to the class
* 20/08/2022(v3.7) - Added more logs to the Requests Class
* 21/08/2022(v3.8) - Made the scImage Class
* 27/08/2022(v3.9) - Reduced the size of encoded Image
* 30/08/2022(v3.9.5) - Bug fixes and Improvements
* 24/09/2022(v3.9.6) - Bug fixes and Improvements
* 25/09/2022(v3.9.7) - Bug fixes and Improvements
* 26/09/2022(v3.9.9) - Fixed many bugs in scCloudRequests
* 14/12/2022(v4.0.0) - Fixed the arguments bug in the Cloud Requests feature
* 15/12/2022(v4.0.0) - Bug fixes and improvements in the Cloud Requests feature
* 24/15/2022(v4.1) - Bug fixes
* 10/02/2023(v4.5) - Updated the CloudRequests feature and made it faster
* 11/02/2023(v4.5) - First stable release of the Cloud Requests feature
* 13/02/2023(v4.5.2) - Bug fixes

### Credits:

**This library is made by [@Sid72020123](https://scratch.mit.edu/users/Sid72020123/) on Scratch. Also, thanks to all
contributors.**

### Contributors:

***The names of persons below are their Scratch Usernames.***

| **Person**      | **Role**      | **Contribution**                                                                      |
|-----------------|---------------|----------------------------------------------------------------------------------     |
| **Sid72020123** | *Owner*       | Made the library and most of its features                                             |
| **Ankit_Anmol** | *Contributor* | Fixed some things in the documentation and added some features                        |
| **Chiroyce**    | *Contributor* | Added some features and cleaned up some code                                          |
| **god286**      | *Contributor* | Fixed mistakes in the documentation                                                   |
| **mbrick2**     | *Contributor* | Fixed Badge Consistency and added the Aviate status feature                           |
| **AidanER1**    | *Contributor* | Updated the CloudConnection class and fixed some bugs                                 |
| **Senievol**    | *Idea*        | Gave the trick to make the encoded image data length much lower in Cloud Requests     |
| **awesome-llama**| *Idea*       | Gave the trick to make the encoded image data length much lower in Cloud Requests     |
| **PPPDUD**      | *Contributor* | Fixed mistakes in the documentation                                                   |

*If I'm missing some people and their work in the contributors table, please contact Sid72020123 on Scratch*

