# Session ID Guide

???+ question "What is session ID?"

	Sesssion ID is a type of cookie value that is set by the Scratch website on your local computer

	The website uses the Session ID as a type of security check, i.e, for example, if you follow a user or post a comment, the Scratch website first checks if the session ID of your account is correct and then allows you to perform that action

	The Scratch API not only uses the session ID to validate/check the requests but also certain other cookie values which are equally important as the session ID but the ScratchConnect library requires only the session ID using which it fetches the other cookie types!
	
	*Note: The session ID automatically changes (maybe sometimes) when you login to the Scratch website*
	
## Steps to get the Session ID

Following are the 2 ways using which you can get the session ID of your account:

### Using the Python Code

You can login using ScratchConnect locally on your computer, using the code below:

```python title="get_session_id.py"
import scratchconnect

# Replace the placeholders below with you actual Scratch information

session = scratchconnect.ScratchConnect("Username", "Password")

with open("session_id.txt", "w") as file:
	file.write(session.session_id) # Write the session ID in a text file called "session_id.txt"

# You can open the text file and read/copy the session ID
```	

### From your browser

Follow the steps:

*(It is advised to follow only the steps below when you open the developer tools to keep your account secure, if you don't know what you're doing. Remember: Never share your session ID with anyone!)*

1. Login to the [Scratch](https://scratch.mit.edu/) website
2. Open the developer tools by right clicking anywhere on the page and by clicking the *"Inspect"* option. You can open the developer tools on `Windows` OS using the shortcut `Control + Shift + C` and on `Mac` OS using the shortcut `Command + Option + C` depending on your browser
3. Once you're done, follow the steps according to your browser:

	> For `Firefox` browser: 
	>	> Click the `Storage` tab; In the `Cookies` section click the Scratch website's name. There you will find a key with the name as `scratchsessionsid`. Copy the value corresponding value to that key. This is your session ID
	
	>	>	Image *(The cookie values are censored(in red) for security)*: ![image](/assets/images/get_session_id_firefox.png)


	
	> For `Chrome` browser: 
	>	> Click the `Application` tab; In the `Storage` section, click the `Cookies` option and then the Scratch website's name. There you will find a key with the name as `scratchsessionsid`. Copy the value corresponding value to that key. This is your session ID
	
	>	>	Image *(The cookie values are censored(in red) for security)*: ![image](/assets/images/get_session_id_chrome.png)
	
## Final Important Note

The session ID is very important. **Do NOT share it with anyone.**

Also, remember to store the session ID in `environment` variables if you are using/running the code in online IDEs like [replit](https://replit.com)!

While sharing your code, make sure that you remove the sensitive information from your file!