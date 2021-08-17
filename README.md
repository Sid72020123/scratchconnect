# scratchconnect v1.5

Python Library to connect Scratch API and much more.

This library can show the statistics of Users, Projects, Studios, Forums and also connect and set cloud variables of a
project!

This library needs a Scratch account. Visit the Scratch Website: [https://scratch.mit.edu/](https://scratch.mit.edu/)

![https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

[![PyPI Latest Release](https://img.shields.io/pypi/v/scratchconnect.svg)](https://pypi.org/project/scratchconnect/)
[![Package Status](https://img.shields.io/pypi/status/scratchconnect.svg)](https://pypi.org/project/scratchconnect/)
[![Downloads](https://static.pepy.tech/personalized-badge/scratchconnect?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads)](https://pepy.tech/project/scratchconnect)

### Documentation

Documentation coming soon.......

### Creating a Simple Connection:

Following is a simple program to make a simple connection:

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
```

It will give an error if the `username` or `password` is invalid.

### More Uses:

##### Note:- The below code can be only used by the logged in Scratcher. To get the stats of other users see the User Connection Documentation

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
user.get_id()  # Returns the ID of the user
user.get_messages_count()  # Returns the messages count of the user
user.get_messages(all=False, limit=20, offset=0, filter="all")  # Returns the messages
user.get_work()  # Returns the 'What I am working on' of a Scratch profile
user.get_bio()  # Returns the 'About me' of a Scratch profile
user.get_status()  # Returns the status(Scratcher or New Scratcher) of a Scratch profile
user.get_joined_date()  # Returns the joined date of a Scratch profile
user.get_country()  # Returns the country of a Scratch profile
user.get_featured_data()  # Returns the featured project data of the Scratch profile
user.get_projects()  # Returns the list of shared projects of a user
user.get_follower_count()  # Returns the follower count of a user
user.get_following_count()  # Returns the following count of a user
user.get_total_views()  # Returns the total views count of all the shared projects of a user
user.get_total_loves()  # Returns the total loves count of all the shared projects of a user
user.get_total_favourites()  # Returns the total favourites count of all the shared projects of a user
user.get_following()  # Returns the list of the user following
user.get_followers()  # Returns the list of the user followers
user.get_favourites()  # Returns the list of the user favourites
user.toggle_commenting()  # Toggle the commenting of the profile
user.follow_user(username="Sid72020123")  # Follow a user
user.unfollow_user(username="Sid72020123")  # UnFollow a user
user.set_bio(content="Hi!")  # Set the bio or 'About Me' of the profile
user.set_work(content="Hi!")  # Set the status or 'What I am Working On' of the profile
user.get_all_data()  # Returns all the data of the user
user.get_site_health()  # Returns the health of the Scratch Website.
user.get_news()  # Returns the news of the Scratch Website.
user.get_front_page_projects()  # Returns the front page projects of the Scratch Website.
user.explore_projects(mode="trending", query="*")  # Explore the projects
user.explore_studios(mode="trending", query="*")  # Explore the studios
user.search_projects(mode="trending", search="*")  # Search the projects
user.search_studios(mode="trending", search="*")  # Search the studios
user.set_featured_project(project_id="1", label='featured_project')  # Set the 'Featured Project' of a Scratch Profile
user.get_user_follower_history()  # Return the follower history of the user
user.get_comments(limit=5, page=1)  # Get comments of the profile of the user
```

### Connect a Scratch User:

To connect a Scratch User use the `connect_user()` function. Use the following program to connect a Scratch User:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Username", "Password")
user = login.connect_user(username="Sid72020123")
user.get_id()  # Returns the ID of the user
user.get_messages_count()  # Returns the messages count of the user
user.get_work()  # Returns the 'What I am working on' of a Scratch profile
user.get_bio()  # Returns the 'About me' of a Scratch profile
user.get_status()  # Returns the status(Scratcher or New Scratcher) of a Scratch profile
user.get_joined_date()  # Returns the joined date of a Scratch profile
user.get_country()  # Returns the country of a Scratch profile
user.get_featured_data()  # Returns the featured project data of the Scratch profile
user.get_projects()  # Returns the list of shared projects of a user
user.get_follower_count()  # Returns the follower count of a user
user.get_following_count()  # Returns the following count of a user
user.get_total_views()  # Returns the total views count of all the shared projects of a user
user.get_total_loves()  # Returns the total loves count of all the shared projects of a user
user.get_total_favourites()  # Returns the total favourites count of all the shared projects of a user
user.get_following()  # Returns the list of the user following
user.get_followers()  # Returns the list of the user followers
user.get_favourites()  # Returns the list of the user favourites
user.get_user_follower_history()  # Return the follower history of the user
user.post_comment(content="Hi!")  # Post a comment on the user's profile
user.report(field="")  # Report a user
user.get_all_data()  # Returns all the data of the user
user.get_comments(limit=5, page=1)  # Get comments of the profile of the user
```

### Connect a Scratch Studio:

To connect a Scratch Studio use the `connect_studio()` function. Use the following program to connect a Scratch Studio:

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
studio = user.connect_studio(studio_id=1)
studio.get_id()  # Returns the studio ID
studio.get_title()  # Returns the studio title
studio.get_owner()  # Returns the studio owner
studio.get_description()  # Returns the studio description
studio.get_visibility()  # Returns the studio visibility
studio.get_public()  # Returns whether a studio is public
studio.get_open_to_all()  # Returns whether a studio is open to all
studio.get_comments_allowed()  # Returns whether a studio has comments allowed
studio.get_history()  # Returns the history of the studio
studio.get_stats()  # Returns the stats of the studio
studio.get_thumbnail_url()  # Returns the thumbnail URL of the studio
studio.add_project(project_id=1)  # Add a project to a studio
studio.remove_project(project_id=1)  # Remove a project from a studio
studio.open_to_public()  # Open the studio to public
studio.close_to_public()  # Close the studio to public
studio.follow_studio()  # Follow the studio
studio.unfollow_studio()  # UnFollow the studio
studio.toggle_commenting()  # Toggle the commenting of the studio
studio.post_comment(content="Hi!")  # Post comment in the studio
studio.delete_comment()  # Delete comment in the studio
studio.report_comment(comment_id=1)  # Report comment in the studio
studio.invite_curator(username="Sid72020123")  # Invite a user to the studio
studio.accept_curator()  # Accept the curator invitation in a studio
studio.promote_curator(username="Sid72020123")  # Promote a user in the studio
studio.set_description(content="Hi!")  # Set the description of a Studio
studio.set_title(content="Hi!")  # Set the title of a Studio
studio.get_projects(all=False, limit=40, offset=0)  # Get the projects of the studio
studio.get_comments(all=False, limit=40, offset=0)  # Get the comments of the studio
studio.get_curators(all=False, limit=40, offset=0)  # Get the curators of the studio
studio.get_managers(all=False, limit=40, offset=0)  # Get the managers of the studio
studio.get_activity(all=False, limit=40, offset=0)  # Get the activity of the studio
```

### Connect a Scratch Project:

To connect a Scratch Project use the `connect_project()` function. Use the following program to connect a Scratch
Project:

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
project = user.connect_project(project_id=1)
project.get_author()  # Returns the author of the project
project.get_title()  # Returns the title of the project
project.get_notes()  # Returns the notes(Notes or Credits) of the project
project.get_instruction()  # Returns the instructions of the project
project.get_comments_allowed()  # Returns whether the comments are allowed in a project
project.get_views_count()  # Returns the views count of a project
project.get_loves_count()  # Returns the loves count of a project
project.get_favourites_count()  # Returns the favourites count of a project
project.get_remixes_count()  # Returns the remixes count of a project
project.get_history()  # Returns the history of a project
project.get_remix_data()  # Returns the remix data of a project
project.get_visibility()  # Returns whether the project is visible
project.get_is_public()  # Returns whether the project is public
project.get_is_published()  # Returns whether the project is published
project.get_thumbnail_url()  # Returns the thumbnail url of a project
project.get_assets_info()  # Returns the Assets info of a project
project.get_scripts()  # Returns the scripts of a project
project.love()  # Love a project
project.unlove()  # UnLove a project
project.favourite()  # Favourite a project
project.unfavourite()  # UnFavourite a project
project.get_comments(all=False, limit=40, offset=0, comment_id=None)  # Returns the list of comments of a project
project.get_remixes(all=False, limit=20, offset=0)  # Returns the list of remixes of a project
project.post_comment(content="Hi!")  # Post a comment
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

### Connect a Scratch Forum:

To connect a Scratch Forum use the `connect_forum_topic()` function. Use the following program to connect a Scratch
Forum:

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Username", "Password")
forum = user.connect_forum_topic(forum_id=1)
forum.get_id()  # Returns the id of the forum
forum.get_title()  # Returns the title of the forum
forum.get_category()  # Returns the category of the forum
forum.get_closed()  # Returns whether the forum is closed or not
forum.get_deleted()  # Returns whether the forum is deleted or not
forum.get_time()  # Returns the activity of the forum
forum.get_post_count()  # Returns the total post count of the forum
forum.follow()  # Follow a Forum
forum.unfollow()  # Unfollow a Forum
```

### Bug Reporting:

All Bugs to be reported on my [Scratch Profile](https://scratch.mit.edu/users/Sid72020123/)
or [Github](https://github.com/Sid72020123/scratchconnect/issues)
