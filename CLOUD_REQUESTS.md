# ScratchConnect Cloud Requests v1.0 (beta)

This new feature was first released in version ```4.0.0``` of the ScratchConnect Python Library!

I was inspired to make this feature from @TimMcCool's scratchattch Python library.

**Using this feature, you will be able to send data to-and-from the Scratch project and your Python program.**

**Features:**
* Send any length of data without any data loss! (Tested in a good internet connection)
* Supports any number of arguments sent from the Scratch Project
* You can send any number of data length (or almost unlimited characters of data) to the Scratch Project in much less time!
* This feature is more fast compared to the Cloud Storage feature of this library
* This feature can handle many requests being sent at the same time using a queue system
* It has a built-in way to encode and send images to the Scratch Project!
* Other than ```str``` and ```int``` return data types, it also supports ```list``` and ```dict```(only the dictionary values are sent to the project). ```int``` values are not encoded which reduces the response time
* It also have an events feature
* And more...

**This feature also needs a Scratch script/code to make it work. The Scratch script can be found [here](https://scratch.mit.edu/projects/720252660/)**

In that Scratch Project, click "See Inside" and scroll to the extreme top-left to read the instructions. Please read them while using that...

## Setup:
You have to make a setup using your Python program, like:

### Basic Setup:
```python
```

### Enable Logs:
This feature also has logs where it prints the events. See the following code to enable them:
```python
```

## Examples of Cloud Requests:
### Simple Ping - Pong and basic math:

**Python:**

**Scratch:**

### Sending Simple stats of a user:

**Python**

**Scratch**

### Sending PFP of any user to the project:

**Python**

**Scratch**

## Cloud Events:
This feature also has Cloud Events. See example:
```python
```

## Thank you!
I am excited to see what you create!
