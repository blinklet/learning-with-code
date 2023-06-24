title: Use pipx to Install a Python Program as a CLI Command
slug: install-package-cli-program-pipx
summary: It is more convenient to run a Python program from the terminal prompt instead of as a Python program in its virtual environment. This post shows you how to use *pipx* to install Python packages as command-line-programs.
date: 2021-02-14
modified: 2021-02-14
category: Python
status: published

*[azruntime](https://github.com/blinklet/azure-scripts/tree/main/azruntime#azruntime)*, the Python program I wrote to manage virtual machines in my Azure subscriptions, is more convenient to use when run as a command from the Linux prompt instead of as a Python program in its virtual environment. You can install Python packages as command-line-programs using *[pipx](https://github.com/pipxproject/pipx#pipx--install-and-run-python-applications-in-isolated-environments)*. 

To make *azruntime* work after using *pipx* to install it, I had to organize the project into a proper Python package folder structure, add an [entry point](https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html#the-console-scripts-entry-point) in the *setup.py* file, and change the authentication class used by *azruntime*.

This post describes what I learned about *pipx* and [Python packaging](https://github.com/pypa/packaging.python.org#python-packaging-user-guide) to enable me to install *azruntime* as a CLI application.

<!--more-->

## Changing the package directory structure

I originally structured the *azruntime* package so all its files were in one folder. I know this is not the standard way that packages are organized but I thought it was simpler and it worked with *pip*. However, *pipx* requires the correct package folder structure.

Below, I show the new folder structure I created.

```
azruntime/
├── LICENSE
├── README.md
├── azruntime
│   ├── __init.py__
│   ├── __main__.py
│   └── azruntime.py
├── requirements.txt
└── setup.py
```

At the top level, I have a project folder named "azruntime". This can have any name and I could have called it "azruntime-project" to make it clearer. The top level project folder name is not relevant to packaging.

In the project folder, I have the Python package folder, named "azruntime" and the *setup.py* file. I also have other project files like the LICENSE and README files, and the requirements file.

The *\_\_main\_\_.py* file runs when you run the package using the `python -m azruntime` command. It's not needed for users who will install the package as a command-line tool using *pipx* but it's helpful to have during development. The function import statement in *\_\_main\_\_.py* contains the same expression you will use when adding an entry point in the *setup.py* file.

The *\_\_main\_\_.py* contents is listed below:

```
from azruntime.azruntime import main
main()
```

As you can see, it just imports and runs the *main()* function from the *azruntime.py* module in the *azruntime* package folder.

## Entry Point in setup.py file

*Pipx* sets up a CLI command that runs a function in a Python module. The command passes arguments to the function using the normal Python argument passing methods. You need to tell *pipx* which function to use by defining an *entry point* in the *setup.py* file. In this case, I want *pipx* to set up a command that runs the same *main()* function that the *\_\_main\_\_.py* uses. 

> **NOTE:** The *\_\_main\_\_.py* file and the entry point in the *setup.py* file do not need to point to the same functions. For example, you may use *\_\_main\_\_.py* for testing purposes and have it run a different function.

I added the following line to my *setup.py* file:

```
entry_points = {'console_scripts': ['azruntime=azruntime.azruntime:main'],},
```

I have one console script listed as an entry point. You could create multiple command-line programs using different functions from the same package just by adding them as additional console scripts in the *entry_points* line in the *setup.py* file.

I list the new *setup.py* file below:

```
from setuptools import setup

setup(
    name='AzRuntime',
    url='https://github.com/blinklet/azure-scripts/azruntime',
    packages=['azruntime'],
    install_requires=[
        'wheel',
        'azure-identity',
        'azure-mgmt-resource',
        'azure-mgmt-compute',
        'azure-mgmt-monitor',
        'azure-cli-core',
        'tabulate'
    ],
    version='0.4',
    license='GPLv3',
    description='Print a list of all running VMs in your subscriptions.',
    long_description=open('README.md').read(),
    entry_points = {
        'console_scripts': ['azruntime=azruntime.azruntime:main'],
    },
)
```

## Azure CLI authentication and pipx

After installing *azruntime* with *pipx*, I got an error when I ran the *azruntime* command. It seems that the *AzureCliCredential* class cannot see the user's existing Azure CLI credentials. When I install the *azruntime* package in its own virtual environment using *pip*, everything works. But when I try to install the package on my system using *pipx*, it does not work.

I decided to use the *DefaultAzureCredential* class, with arguments that stop it from running the other authentication methods. I then enable the method that allows the user to start an interactive Azure login. 

In the *[azruntime.py](https://github.com/blinklet/azure-scripts/tree/main/azruntime)* module, I replaced the line:

```
credentials = AzureCliCredential()
```

with the following statement:

```
credentials = DefaultAzureCredential(
    exclude_environment_credential = True,
    exclude_managed_identity_credential = True,
    exclude_shared_token_cache_credential = True,
    exclude_visual_studio_code_credential = True,
    exclude_interactive_browser_credential = False
)
```

The new version of the *azruntime* script will check for existing Azure CLI credentials (if it is installed as a Python package using *pip*) and, if that is not working, it will start a web browser and allow the user to login interactively. So, if you install it using *pipx*, you will always have to authenticate using a web browser every time you run the *azruntime* command.

> **Help requested:** I cannot find the reason why the *AzureCliCredential* class does not work if the package is installed using *pipx*. If you know, please post something in the comments below.

## Using pipx

Now I can create a system-level command taht runs the *azruntime* program in its own virtual environment, but I do not need to activate a virtual environment, myself. *Pipx* makes it easier to distribute and use Python programs.

*Pipx* relies on *pip* and *venv* so you may need to install them:
```
sudo apt install python3-venv
sudo apt install python3-pip
```

Do not install *pipx* using your Linux system's package manager like *dnf* or *apt*. You'll get an old version that does not work. Instead, [install *pipx* from PyPI](https://pypi.org/project/pipx/) as follows:

```
python3 -m pip install pipx
python3 -m pipx ensurepath
```

Then, install *azruntime* with the following command:

```
pipx install "git+https://github.com/blinklet/azure-scripts.git#egg=azruntime&subdirectory=azruntime"
```

Now, you can run the *azruntime* Python program from your Linux command line kust by typing the command:

```
$ azruntime
```

## Conclusion

I changed that way users can install *azruntime* so they can install it as a command-line utility on their Linux systems. The same procedure should work also for Windows and Mac systems -- with some differences in the way *pip*, *venv* and *pipx* are installed.
