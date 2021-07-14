# scratchconnect v1.0

Python Library to connect Scratch API and much more.

This library can show the statistics of Users, Projects, Studios, Forums and also connect and set cloud variables of a
project!

This library needs a Scratch account. Visit the Scratch Website: [https://scratch.mit.edu/](https://scratch.mit.edu/)

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
```

### Connect a Scratch User:

To connect a Scratch User use the `connect_user()` function. Use the following program to connect a Scratch User:

```python
import scratchconnect

login = scratchconnect.ScratchConnect("Sid_tutorials", "Siddhesh_38856541")
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
```

### Connect a Scratch Studio:

To connect a Scratch Studio use the `connect_studio()` function. Use the following program to connect a Scratch Studio:

```python
import scratchconnect

user = scratchconnect.ScratchConnect("Sid_tutorials", "Siddhesh_38856541")
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
```
