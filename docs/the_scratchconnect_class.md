# The ScratchConnect class

The `ScratchConnect` class is the main class of the library. **It is essential in every program using the library.**

Once you finished the login part, you can now use the library!

Example to get the data of the logged in user:

```python title="user_data.py"
import scratchconnect

session = scratchconnect.ScratchConnect("Username", "Password")

all_data = session.all_data() # Get the profile data of the logged in user in 'dict' format

print(all_data)
```

???+ question "But what if I haven't logged in using ScratchConnect? How do I get the user data?"
	No worries :)

	Try the following code:

	```python title="nologin_user_data.py"
	import scratchconnect

	session = scratchconnect.ScratchConnect() # Leave the arguments blank

	user = session.connect_user("griffpatch") # Connect a user. For eg., "griffpatch"

	all_data = user.all_data() # Get the profile data of the user in 'dict' format

	print(all_data)
	```
## Properties/Parameters

### `#!python username: str | None`

The username to login

### `#!python password: str | None`

The password of that username to login

### `#!python cookie: dict | None`

The cookie if you are [logging in with cookie](/getting_started/#cookie-login)

### `#!python auto_cookie_login: bool`

Set it to `#!python True` if you are using [advanced cookie login](/getting_started/#advanced-cookie-login)

### `#!python online_ide_cookie: dict | None`

The cookie if you are [logging in using an online IDE](/login_in_replit)

## Methods

!!! note "Important Note"
	**Some of the methods below use the Scratch DB API to fetch the information which may not be always up to date and may raise errors if the Scratch DB API is down!**

	Some of the methods below require login either using `username and password` or `cookie` and will raise an error if you use those methods/functions without login!

### `update_data()`

The function to update the data of the logged in user

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	session.update_data()
	```		

### `id()`

Returns the ID of the logged in user in `#!python int` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.id())
	```

### `thumbnail_url()`

Returns the thumbnail URL data of the logged in user in `#!python dict` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.thumbnail_url())
	```

### `messages_count()`

Returns the messages count of the logged in user in `#!python int` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.messages_count())
	```

### `work()`

Returns the 'What I am working on' section of the profile in `#!python str` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.work())
	```

### `bio()`

Returns the 'About me' section of the profile in `#!python str` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.bio())
	```

### `status()`

Returns whether the logged in user has a `Scratcher` or a `Non Scratcher` status in `#!python str` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.status())
	```

### `joined_date()`

Returns the joined date of a Scratch profile in `#!python str` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.joined_date())
	```

### `country()`

Returns the country of a Scratch profile in `#!python str` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.country())
	```

### `followers_count()`

Returns the follower count of a user in `#!python int` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.followers_count())
	```

### `following_count()`

Returns the following count of a user in `#!python int` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.following_count())
	```

### `total_views()`

Returns the total views count of all the shared projects of a user in `#!python int` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.total_views())
	```

### `total_loves_count()`

Returns the total loves count of all the shared projects of a user in `#!python int` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.total_loves_count())
	```

### `total_favourites_count()`

Returns the total favourites count of all the shared projects of a user in `#!python int` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.total_favourites_count())
	```

### `projects_count()`

Returns the total shared projects of the user in `#!python int` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.projects_count())
	```

### `featured_data()`

Returns the featured project data of the Scratch profile in `#!python dict` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.featured_data())
	```

### `projects(all, limit, offset)`

Returns the list of shared projects of a user in `#!python list` format

**Parameters**

| Name   | Description                                                       | Required | Default Value |
|--------|-------------------------------------------------------------------|----------|---------------|
| all    | Set it to True if you want to fetch all the projects of that user | No       | `False`       |
| limit  | The number of projects you want to fetch                          | No       | 20            |
| offset | The number of projects to be skipped from the beginning           | No       | 0             |

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.projects(all=False, limit=20, offset=0))
	```

### `following(all, limit, offset)`

Returns the list of Scratchers the user is following in `#!python list` format

**Parameters**

| Name   | Description                                                       | Required | Default Value |
|--------|-------------------------------------------------------------------|----------|---------------|
| all    | Set it to True if you want to fetch all the following of that user| No       | `False`       |
| limit  | The number of users you want to fetch                             | No       | 20            |
| offset | The number of users to be skipped from the beginning              | No       | 0             |

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.following(all=False, limit=20, offset=0))
	```

### `followers(all, limit, offset)`

Returns the list of Scratchers the user is followed by in `#!python list` format

**Parameters**

| Name   | Description                                                       | Required | Default Value |
|--------|-------------------------------------------------------------------|----------|---------------|
| all    | Set it to True if you want to fetch all the followers of that user| No       | `False`       |
| limit  | The number of users you want to fetch                             | No       | 20            |
| offset | The number of users to be skipped from the beginning              | No       | 0             |

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.followers(all=False, limit=20, offset=0))
	```

### `favourites(all, limit, offset)`

Returns the list of projects the user has favourited in `#!python list` format

**Parameters**

| Name   | Description                                                       			| Required | Default Value |
|--------|------------------------------------------------------------------------------|----------|---------------|
| all    | Set it to True if you want to fetch all the favourite projects of that user  | No       | `False`       |
| limit  | The number of projects you want to fetch                            			| No       | 20            |
| offset | The number of projects to be skipped from the beginning             			| No       | 0             |

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.favourites(all=False, limit=20, offset=0))
	```

### `user_follower_history(all, limit, offset)`

Returns the follower history of the user in `#!python list` format

**Parameters**

| Name    | Description                             | Required | Default Value |
|---------|-----------------------------------------|----------|---------------|
| segment | The length of time between each segment | No       | ""            |
| range   | Of how far back to get history          | No       | 30            |

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.user_follower_history(segment="", range=30))
	```

### `all_data()`

Returns all the data of the user in `#!python dict` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.all_data())
	```


!!! note
	Remember to call the `update_data()` function when you need to update the data!

### `ocular_data()`

Returns the [ocular](https://ocular.jeffalo.net) data of the user in `#!python dict` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.ocular_data())
	```

### `aviate_data()`

Returns the [aviate](https://aviateapp.eu.org) data of the user in `#!python dict` format

**Parameters**

| Name | Description                        | Required | Default Value |
|------|------------------------------------|----------|---------------|
| code | True to get the code of the status | No       | `False`       |

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.aviate_data(code=False))
	```

### `comments()`

Returns the comments on the user's profile

**Parameters**

| Name  | Description | Required | Default Value   |
|-------|-------------|----------|-----------------|
| limit | The limit   | No       | 5 (recommended) |
| page  | The page    | No       | 1               |

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.comments(limit=5, page=1))
	```

### `messages()`

Returns the messages of the logged in user in `#!python dict` format

**Parameters**

| Name   | Description                                                                   | Required | Default Value |
|--------|-------------------------------------------------------------------------------|----------|---------------|
| all    | Set it to `True` if you want to fetch all the messages                        | No       | `False`       |
| limit  | The limit of messages you want to get if you're not using the `all` parameter | No       | 20            |
| offset | The number of messages to skip from the beginning                             | No       | 0             |
| filter | Filter the messages                                                           | No       | `""`          |

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.messages(all=True)) # Get  all the messages
	
	print(session.messages(limit=10, offset=0)) # Get the first 10 messages
	
	print(session.messages(limit=10, offset=5)) # Get 10 messages skipping 5 from the beginning
	```

### `clear_messages()`

Clears the messages (count) of the logged in user and returns the response in `#!python str` format

??? info "Example"
	```python
	import scratchconnect

	session = scratchconnect.ScratchConnect("Username", "Password")

	print(session.clear_messages())
	```

### WIP...