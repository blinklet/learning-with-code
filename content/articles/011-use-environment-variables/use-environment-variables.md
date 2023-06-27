title: Use environment variables to protect your secrets
slug: use-environment-variables-python
summary: How Python programmers can set and use environment variables to improve their programs' flexibility and security
date: 2023-04-07
modified: 2023-04-07
category: Python
status: published

Environment variables are key-value pairs that are are set outside of a Python program but may be accessed by the program during its execution. They are part of the operating system environment in which a Python program runs and are usually used to store information that is unique to a system, such as paths to important directories, credentials, API keys, or database connection strings.

If you use environment variables, you must set them before you execute your program, using the operating system's command line interface, by editing a configuration file, or, in the case of cloud-based platforms, via a web interface or API. Programmer use functions like those found in [Python's os module](https://docs.python.org/3/library/os.html) to access environment variables in their programs. This post describes how Python programmers can set and use environment variables to improve their code's flexibility and security.

## Why use environment variables

There are many reasons to use environment variables instead of just hard-coding program configuration information in your program's source code or in a separate configuration file. For individual Python programmers, the most relevant reasons are:

1. Security
2. Separation of configuration from code

### Security

Normally, you do not want to reveal sensitive information like passwords, database credentials, or API keys to anyone who looks at your code. This is especially true when writing code that will be part of an open-source project, or may be stored in a public source code repository. 

Environment variables offer a [relatively secure way](https://www.getfishtank.com/blog/best-practices-for-committing-env-files-to-version-control) to avoid publishing in your source code the secrets your program needs to access sensitive resources like databases and APIs. Your program reads the secrets from its environment when the it runs.

After you get experience working with environment variables you can explore some [even more secure ways](https://tratnayake.dev/how-to-securely-work-with-secrets-during-development) to store, access, and distribute secrets to your applications.

### Separation of configuration from code

Environment variables provide a convenient way to [manage configuration settings for Python programs](https://12factor.net/config). You can change configuration settings in your environment without modifying your source code. This makes it easy to deploy a program to different environments like development, test, or production, each of which may use different resources.

## How to set environment variables for your program

Environment variables are usually set by system operators when they set up the environment in which your python program will be deployed. This process can be automated on some platforms. Individual developers will usually set environment variables on their own development systems and [the procedure will be different](https://www.twilio.com/blog/how-to-set-environment-variables-html) for different operating systems or cloud platforms.

On a Linux system, for example, you would enter the following commands in the Bash shell to configure environment variables and run the program:

```bash
(env) $ export DB_SERVER=server.name.com
(env) $ export DB_NAME=database_name
(env) $ export DB_UID=username
(env) $ export DB_PWD=password
(env) $
(env) $ python my_program.py
```

Using the same example on a Windows system, you would enter the following commands into the Powershell terminal:

```powershell
(env) > $Env:DB_SERVER = 'server.name.com'
(env) > $Env:DB_NAME = 'database_name'
(env) > $Env:DB_UID = 'username'
(env) > $Env:DB_PWD = 'password'
(env) >
(env) > python my_program.py
```

When you set environment variables this way, they are not permanent and will disappear when you close the environment; for example, when you close your terminal window.

I do not discuss how to permanently set environment variables in this post because it can be done [multiple ways on each type of system](https://www3.ntu.edu.sg/home/ehchua/programming/howto/Environment_Variables.html) and I think that using *.env* files (see below) is the better way for programmers to manage persistent environment variables.

## Protecting secrets

To keep from losing or forgetting secrets, developers will usually encrypt and store them in a digital vault like [Bitwarden](https://bitwarden.com/), [1Password](https://1password.com/), or [Vault](https://developer.hashicorp.com/vault/docs/what-is-vault) and then they may manually assign those secrets to environment variables before they test their programs.

If you plan to deploy your program in the cloud, you may store secrets in a tool like [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts) or [Google Secrets Manager](https://cloud.google.com/architecture/security-foundations/keys-secret-management), which would then automatically set up environment variables when you deploy your program on their cloud platforms.

For developers, there is a simple and secure method for storing secrets used to set environment variables in the development system: a *dotenv* file.

## *Dotenv* files

A [*dotenv* file](https://dev.to/nicat/using-dotenv-env-in-python-4l49) is a file named *.env* and is placed in your development project's root folder. When developing your Python program on your local computer, store secrets used to set environment variables in your project's *.env* file. Then, in your program, use the *[python-dotenv](https://pypi.org/project/python-dotenv/)* package to load variables from either the *.env* file or from the program's environment.

To avoid having to tediously re-enter your environment variables every time you start a new environment, I recommend you use an *.env* file when developing your program.

### Install the *python-dotenv* package

Install the *[python-dotenv](https://pypi.org/project/python-dotenv/)* package in your Python project's [virtual environment](https://realpython.com/python-virtual-environments-a-primer/).

```bash
(env) $ pip install python-dotenv
```

### Create the *.env* file

Create two files named *.env* and *.env.example* in the project's root folder. 

Other programmers who may use your code still need to know which variables need to be set. Adding an [example *.env* file](https://www.twilio.com/blog/environment-variables-python) with a name such as ".env.example" to your repository provides guidance to your users, without giving away sensitive information. [^1]

[^1]: From Twilio blog post [Working with Environment Variables in Python](https://www.twilio.com/blog/environment-variables-python), accessed in June 2023

The contents of the *.env.example* file would look like the following:

```bash
DB_SERVER=server.name.com
DB_NAME=database_name
DB_UID=username
DB_PWD=password
```

The contents of the *.env* file would have the same variable names, but contain the actual values needed for your program to work. For example, it might look like the following, if you are providing SQL Server database information:

```bash
DB_SERVER=mydatabaseserv.microsoft.com
DB_NAME=race_car_db
DB_UID=brian56
DB_PWD=tanJ451Gr0k
```

Save the files.

### Except *.env* files from source control

If you use a source control system, use the appropriate method to ensure it does not copy the *.env* file into its database. For example, if you use Git for source control, add `.env` to the *.gitignore* file in your project folder to ensure your secrets are not recorded in the Git database. This is a critical step required to protect your system's secrets. 

> **WARNING:** It is *CRITICAL* that you configure your source control system to ignore your *.env* file. 

The *.env.example* file will still be tracked in your source code repository so it will be available to other users who may clone it from your source control system. 

### Save your *.env* file in a vault

Optionally, you may want to save the contents of your *.env* file in a vault that you can access from any computer. The *.env* file is not tracked in your source control system so it will not be available if you clone your repository to another computer to either deploy or develop it there.

Every vault will operate differently. In my case, I created a note in my personal password manager and copy-and-pasted the contents of the *.env* file into it. Now, when I move my project to another system, I clone the repository then open my password manager and copy the contents of my note into a new *.env* file.


### Use a *.env* file to set environment variables at run time

To use the environment variables from the *.env* file in your program, import the *dotenv.load_dotenv()* function into your program and call it.

```python
from dotenv import load_dotenv

load_dotenv()
```

The *Load_dotenv()* function exports the environment variables in the *.env* file into the program's environment, if they do not already exist. From this point on, you can read environment variables as you usually would, using the *os.getenv()* function.

The *dotenv* module offers you flexibility in handling environment variables in your Python programs. If you are operating in an environment in which the some environment variables have already been set, the *dotenv* module will use them and will not overwrite them with the values in the *.env* file, unless explicitly told to do so.

If you do want to overwrite any existing environment variables with the values in the *.env* file, you may include the parameter *override=True* when and call the *load_dotenv()* function. 

## How to access environment variables in your program

Regardless of how environment variables are set, Python programs access them through the [*os* module in the Python Standard Library](https://docs.python.org/3/library/os.html#os.getenv), which provides functions for interacting with the operating system. 

Use the *os.getenv()* builtin function in your program to get the value associated with each environment variable. For example:

```python
import os

database_server = os.getenv('DB_SERVER')
database_name = os.getenv('DB_NAME')
database_userid = os.getenv('DB_UID')
database_password = os.getenv('DB_PWD')
```

Now you can use the values you read from the environment variables in your program. For example, you might use the values from the above example to build a database connection string that enables you to access data from a database server.

## Conclusion

Environment variables enable you to write more flexible and configurable Python programs that can adapt to different environments without requiring code changes. They provide a convenient way to separate configuration details from your code, making it easier to manage different deployment scenarios. And, most importantly, they enable you to conveniently test your program in your development environment while protecting your system's secrets from being published in your public source code repositories.

Use a *.env* file to load program configurations and secrets into environment variables when you are developing your Python program. Use other methods for setting environment variables when you move your program to a production environment like a cloud server. Most cloud and platform vendors provide a key vault and a user interface that allows programmers to set environment variables in a secure way. 