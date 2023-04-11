# Getting Started

## Basic Setup/Login

Once you have installed `ScratchConnect`, import that using the `import` statement in Python:

```python title="simple_import.py"
import scratchconnect # Import the library

# Replace the "Username" and "Password" placeholders below with you actual Scratch username and password!
session = scratchconnect.ScratchConnect("Username", "Password") # Create a new object of the ScratchConnect class
```

!!! warning "Important Note regarding the usage in online IDEs"
	If you are using online IDEs like [replit](https://replit.com), please use the `environment` variables to store the sensitive information about your Scratch accounts like the `username`, `password` and `session id`.

## Cookie Login

??? question "How to get the session ID?"
	To get the session ID of your account, please read the [Session ID](session_id.md) guide
	
To login with cookie *(In case you don't want to login with your password)*, you can use the cookie login. Example:

```python title="cookie_login.py"
import scratchconnect

# Set a cookie dictionary:

cookie = {
	"Username": "<YOUR USERNAME HERE>", # Replace the placeholder with your username
	"SessionID": "<YOUR SESSION ID HERE>" # Replace the placeholder with your session ID
}

session = scratchconnect.Scratchconnect(cookie=cookie) # Pass the "cookie" dictionary to the cookie parameter of the class
```

**Or more better example would be to store the session ID in a file and then read that in the program. To store the session ID in a file, use [this](/session_id/#using-the-python-code) code. Example:**

```python title="cookie_login.py"
import scratchconnect

session_id = ""
with open("session_id.txt", "r") as file:
	session_id = file.read()

cookie = {
	"Username": "<YOUR USERNAME HERE>", # Replace the placeholder with your username
	"SessionID": session_id
}

session = scratchconnect.Scratchconnect(cookie=cookie) # Pass the "cookie" dictionary to the cookie parameter of the class
```

!!! note
	**Once you login using a cookie, the library may give a warning just to inform you that some features of the library may not work if the cookie values are wrong!**

!!! warning "Important Note regarding the use of Cookie Login"
	If you are using cookie login in online IDEs like [replit](https://replit.com), please use the `environment` variables to store the sensitive information about your Scratch accounts like the `username`, `password` and `session id`.

## Advanced Cookie Login

??? question "How to get the session ID?"
	To get the session ID of your account, please read the [Session ID](session_id.md) guide

This feature is the combination of both the `Basic` and the `Cookie` login

Using this feature, the library will automatically login using a cookie in case the basic login was not successful

Example to use this:

```python title="advanced_cookie_login.py"
import scratchconnect

cookie = {
	"Username": "<YOUR USERNAME HERE>",
	"SessionID": "<YOUR SESSION ID HERE>"
}

session = scratchconnect.ScratchConnect(username="Username", password="Password", cookie=cookie, auto_cookie_login=True) # Set the "auto_cookie_login" parameter of the ScratchConnect class to "True" to enable the advanced login
```

The above code will perform the cookie login if the basic login was unsuccessful!

!!! note
	**Once you login using a cookie, the library may give a warning just to inform you that some features of the library may not work if the cookie values are wrong!**

!!! warning "Important Note regarding the use of Advanced Cookie Login"
	If you are using cookie login in online IDEs like [replit](https://replit.com), please use the `environment` variables to store the sensitive information about your Scratch accounts like the `username`, `password` and `session id`.
	
## No login!

If you don't want to perform the actions such as posting a comment, following a user, etc. and only want to `GET` the data from the Scratch API, then you can use the library without any login!

See an example:

```python title="no_login.py"
import scratchconnect

session = scratchconnect.ScratchConnect() # Leave all the parameters empty to use the library without login!
```

!!! note
	**If you use the library without login, it will just give a `warning` that the basic and cookie login is failed. This is normal and you can still continue running the code/ using the library.**

## Login in replit

To login in [replit](https://replit.com), you have to use another type of login as the Scratch API had recently blocked the requests coming from [replit](https://replit.com)

Read the [Login in replit](/login_in_replit) guide

!!! note "Important Note"
	ScratchConnect will not allow a **banned** account to login and will raise an error.