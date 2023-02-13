# ScratchConnect Cloud Requests

This new feature was first released in version ```4.0.0``` of the ScratchConnect Python Library!

I was inspired to make this feature from @TimMcCool's scratchattach Python library.

**Using this feature, you will be able to send data to-and-from the Scratch project and your Python program.**

**Features:**
* Send any length of data without any data loss! (Tested in a good internet connection)
* Send arguments faster...
* You can send any number of data length (or almost unlimited characters of data) to the Scratch Project in much less time!
* This feature is more fast compared to the Cloud Storage feature of this library
* This feature can handle many requests being sent at the same time using a queue system
* It has a built-in way to encode and send images to the Scratch Project!
* Other than ```str``` and ```int``` return data types, it also supports ```list``` and ```dict```(only the dictionary values are sent to the project). ```int``` values are not encoded which reduces the response time
* It also has an events feature
* And more...

**This feature also needs a Scratch script/code to make it work. The Scratch script can be found [here](https://scratch.mit.edu/projects/801780213/)**

Download that project on your computer and then later upload it on the Scratch Website.

In that Scratch Project, click "See Inside" and scroll to the extreme top-left to read the instructions. Please read them first before using the code...

## Setup:
You have to make a setup using your Python program, like:

### Basic Setup:
```python
import scratchconnect

user = scratchconnect.ScratchConnect(username="Username", password="Password")
project = user.connect_project("<your project id here>") # Connect a project

cloud_requests = project.create_cloud_requests(handle_all_errors=True) # Create a new cloud request. Set the "handle_all_errors" parameter to True if you want to handle all errors...
```

### Enable Logs:
This feature also has logs where it prints the events. See the following code to enable them:
```python
import scratchconnect

user = scratchconnect.ScratchConnect(username="Username", password="Password")
project = user.connect_project("<your project id here>")

cloud_requests = project.create_cloud_requests(handle_all_errors=True, print_logs=True) # Enable the logs by setting the "print_logs" parameter to True
```

## Examples of Cloud Requests:
### Simple Ping - Pong:

**Python:**

```python
import scratchconnect

user = scratchconnect.ScratchConnect(username="Username", password="Password")
project = user.connect_project("<your project id here>")

cloud_requests = project.create_cloud_requests(handle_all_errors=True, print_logs=True)

@cloud_requests.request("ping") # Create a new request name and type
def function1():
    return "pong" # Return a response


cloud_requests.start(update_time=1) # Start the Cloud Requests loop. Here "update_time" is the time after which the cloud request loop should look for a new request
```

Run the above code and make a new request from your Scratch project with the name "ping"

**Scratch:**

Click the following blocks of code to send the request:

![image](https://user-images.githubusercontent.com/70252606/208305060-5e55be1b-7304-4f77-9358-d4c0dedd319f.png)

After the request is complete, you will see the data being received in the project:

![image](https://user-images.githubusercontent.com/70252606/208305350-d72f9c48-6835-4437-a550-9999cc85bec3.png)


### Sending Simple stats of a user:

**Python**

```python
import scratchconnect

user = scratchconnect.ScratchConnect(username="Username", password="Password")
project = user.connect_project("<your project id here>")

cloud_requests = project.create_cloud_requests(handle_all_errors=True, print_logs=True)

@cloud_requests.request("user-stats")
def get_user_data(username):  # Add a parameter to your function
    try:
        u = user.connect_user(username)  # Connect a user on Scratch
        return u.all_data()  # Return the data of the user. Note: this function returns the data in dict form and the cloud requests only sends the values of that dict in list form
    except scratchconnect.Exceptions.InvalidUser:  # Return a message when the user was not found
        return "User doesn't exist!"


cloud_requests.start()
```

**Scratch**

Scratch code:

![image](https://user-images.githubusercontent.com/70252606/208306894-0310b348-b9d6-4638-bc30-7587fe8b28c9.png)

### Sending PFP of any user to the project:

**Python**

```python
import scratchconnect

user = scratchconnect.ScratchConnect(username="Username", password="Password")
project = user.connect_project("<your project id here>")

cloud_requests = project.create_cloud_requests(handle_all_errors=True, print_logs=True)

image = user.create_new_image()  # Create a new scImage object


@cloud_requests.request("user-pfp")
def get_user_pfp(username,
                 size=50):  # You can also add any number of arguments to your function! And default values too!
    image.get_user_image(query=username, size=size)
    return image  # Directly return the image class as a response


cloud_requests.start()
```
And done! Run the script of your Scratch project and all the response data will be stored in the "IMAGE" list on Scratch.

**Scratch**

Scratch Code:

![image](https://user-images.githubusercontent.com/70252606/208308315-ede9f7cd-fafa-4020-9583-b6e466fe2b21.png)


## Cloud Events:
This feature also has Cloud Events. See example:
```python
import scratchconnect

user = scratchconnect.ScratchConnect(username="Username", password="Password")
project = user.connect_project("<your project id here>")

cloud_requests = project.create_cloud_requests(handle_all_errors=True, print_logs=True)

@cloud_requests.event("connect")  # Do something when the cloud requests is connected
def connected():
    print("Connected Cloud Requests!")


@cloud_requests.event("new_request")  # Do something when a new request is made
def new_request():
    print("New Request!", cloud_requests.get_request_info())


@cloud_requests.event("error")  # Do something when there was an error
def error():
    print("Error!")


cloud_requests.start()
```

## Thank you!
I am excited to see what you create!
