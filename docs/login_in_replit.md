# Login in Replit

## Setup

To login on [replit](https://replit.com), you first need to store the session ID of you account in an `environment` variable!

Follow the steps:

1. Read the [session ID](/session_id) guide to get your session ID
2. **Store the session ID in an `environment` variable in replit.** Read [replit's guide](https://docs.replit.com/programming-ide/workspace-features/storing-sensitive-information-environment-variables) if you need any help
3. Read/Call the value of your environment variable in your code. A small guide can be seen [here](https://docs.replit.com/programming-ide/workspace-features/storing-sensitive-information-environment-variables#python)

And you're done! Now you can use the Actual login as documented below:

## Actual Replit Login

To login in [replit](https://replit.com) and other online IDEs, using the following feature:

```python title="login_in_replit.py"
import scratchconnect

# Set a cookie dictionary:

cookie = {
    "Username": "<YOUR USERNAME HERE>", # Replace the placeholder with your username
    "SessionID": "<YOUR SESSION ID HERE>" # Replace the placeholder with your session ID
}

session = scratchconnect.ScratchConnect(online_ide_cookie=cookie) # Pass the "cookie" dictionary to the online_ide_cookie parameter of the class
```

!!! note "Important Note"
	If you login in [replit](https://replit.com), using the `Online IDE Login` feature, only the `GET` type of requests are performed, i.e., you won't be able to perform the interactions to the [Scratch website](https://scratch.mit.edu) like following a user, posting a comment, etc.
	
	This is because this login feature uses a proxy to request the [Scratch API](https://api.scratch.mit.edu) and your login and sensitive user information suchh as `password` and `session_id`, etc. is not sent to the proxy. This is done to keep your data safe.