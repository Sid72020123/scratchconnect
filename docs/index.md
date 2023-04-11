# Introduction and Installation

## Introduction

![banner](https://u.cubeupload.com/Sid72020123/scratchconnect.png)

ScratchConnect is a simple, easy-to-use Scratch API wrapper for **Python**

It is used to _connect_ the Scratch API and get/fetch the information and stats of users, studios, projects, forums, etc. from the [Scratch website](https://scratch.mit.edu/)

Other than just fetching the content, it can also perform some actions like:

* Following a user, studio or a forum topic
* Posting comments on a user's profile or a studio and a project 
* Setting/Changing the cloud variables of a Project directly just using the Python code
* And much more...

!!! warning
	To use this library, you should have the basic knowledge of Python. Using the library without any knowledge can be risky!

**Your login information and cookie values are kept safe and are not sent to any other API or website other than the trusted Scratch APIs**

**The source code of the library can be found on [Github](https://github.com/Sid72020123/scratchconnect)**

## Requirements
* [Python](https://python.org/) version `3.6+`. *Possibly download the latest version*
* Possibly a [Scratch](https://scratch.mit.edu/) account *(In case you need to perform some actions on the site)*

## Installation

To install the library, you can do either one of these:

### Using pip

Type the following command in your `command prompt` or `terminal`:
```
pip install scratchconnect
```

### Directly using the Python Code

Run the following code in Python:
```python title="install.py"
import os
os.system("pip install scratchconnect")
```

??? note "Troubles while Installing?"
	If you have any trobules while installing the library, then visit [this link](https://packaging.python.org/en/latest/tutorials/installing-packages/)

!!! note
	Make sure you update the library from time to time so that you install and use the latest stable version

## Getting Started

If you are a beginner, check out the [Getting Started](/getting_started) guide