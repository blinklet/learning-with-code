title: Packaging Python applications using modern tools
slug: python-packaging-modern
summary: Python packaging has changed over the past few years. In this post, I will update the way my *usermapper* Python package is structured and use modern tools to re-publish it.
date: 2023-09-30
modified: 2023-09-30
category: Python
<!-- status: Published -->

To distribute a Python program so it can be installed using a package manager like *[pip](https://pip.pypa.io/en/stable/)* or *[pipx](https://github.com/pypa/pipx)*, you need to package it. The [Python packaging process](https://packaging.python.org/en/latest/) has [evolved](https://drivendata.co/blog/python-packaging-2023) since I covered my [first experience packaging a Python application]({filename}/articles/005-install-package-cli-program-pipx/install-package-cli-program-pipx.md) several years ago. In this post, I will revisit my *[usermapper]({filename}/articles/002-python-learning-network-engineers/python-learning-network-engineers.md)* project and re-package it using the modern Python packaging process.

## The modern Python packaging tools

The [Python Packaging Authority](https://www.pypa.io/en/latest/) (PyPA) [recommends](https://packaging.python.org/en/latest/guides/tool-recommendations/#packaging-tool-recommendations) the following packaging tools:

* *[pip-tools](https://github.com/jazzband/pip-tools)* contains the *pip-compile*  and *pip-sync* tools that help you manage dependencies in your Python package. I don't use it in this post, but is it useful when you need to create a *requirements.txt* file from your project's metadata or when you need to create a detailed list of all you project's dependencies, including dependencies of dependencies.
* *[setuptools](https://setuptools.pypa.io/en/latest/)* is the recommended "backend" for the Python package creation process.
* *[build](https://pypa-build.readthedocs.io/en/stable/index.html)* provides the "frontend" for the Python package creation process.
* *[twine](https://twine.readthedocs.io/en/latest/)* uploads packages to the PyPI database so they can easily be distributed.

All of the recommended packaging tools use the *[pyproject.toml](https://peps.python.org/pep-0621/)* file in your Python project's directory.

### Alternative tools

There are [many alternative packaging tools](https://packaging.python.org/en/latest/key_projects/#project-summaries) available. The other tools all offer additional functionality and some of them automate part of the [packaging and distribution](https://packaging.python.org/en/latest/tutorials/packaging-projects/) process. The Python community does not seem to agree on which is the best tool for most cases. I will start with the basics and use the tools recommended by the PyPA.




## Project organization

I cloned the original *usermapper* project to my PC from my [GitHub repository](https://github.com/blinklet/usermapper):

```bash
$ git clone https://github.com/blinklet/usermapper.git
```

The current project, organized around the older way of packaging Python programs, has the following structure:

```bash
usermapper
├── config.yaml
├── config.yaml.example
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── test.py
├── usermapper
│   ├── __init__.py
│   ├── __main__.py
│   ├── mapperdata.py
│   └── usermapper.py
└── user-mapping.xml.example
```

I started working on a new git branch named *repack*:

```bash
$ cd usermapper
$ git branch repack
$ git checkout repack
```

I re-organized Python files in my project directory according to the [recommendations](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout) made by the *setuptools* project team:

* I added a *docs* folder so that I can add [project documentation](https://packaging.python.org/en/latest/tutorials/creating-documentation/) in the future. The *config.yaml.example* file serves as partial documentation, for now.
* I added a *src* folder and moved the *usermapper* package into it. 
* I added a *tests* directory and moved the *tests.py* file into it. This is a very basic test script. In the future, after I learn more about adding unit and system tests to Python projects, this directory will contain all the test code. 

The new project structure looks like the listing below. Using this structure allows me to use most of the default settings in *setuptools*.

```bash
usermapper
├── docs
│   └── config.yaml.example
├── LICENSE
├── README.md
├── requirements.txt
├── setup.py
├── src
│   └── usermapper
│       ├── __init__.py
│       ├── __main__.py
│       ├── mapperdata.py
│       └── usermapper.py
└── tests
    ├── config.yaml
    ├── test.py
    └── user-mapping.xml.example
```

I followed the [*setuptools* documentation](https://setuptools.pypa.io/en/latest/userguide/quickstart.html#basic-use) and create a *pyproject.toml* file in a text editor an added the following content to it. Use the [TOML format](https://toml.io/en/).

First, I state the backend that the project will use for packaging. In this case, I am using *setuptools*:

```
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"
```

Next, I add project metadata. This will all be used by the PyPI web site when you upload the package. When building, the main thing you need to look at is the version number. If you try to build on top of an existing version, you can get an error.

```
[project]
name = "usermapper"
version = "0.3"
authors = [{name = "Brian Linkletter", email = "mail@brianlinkletter.ca"}]
description = "Create a manual authentication file for the Guacamole remote access gateway from a simple configuration file."
readme = "README.md"
requires-python = ">=3.7"
keywords = ["Guacamole", "YAML", "XML", "authentication"]
license = {text = "GPLv3"}
classifiers = ["Framework :: Flask", "Programming Language :: Python :: 3"]
dependencies = ["PyYAML"]

[project.urls]
Repository = "https://github.com/blinklet/usermapper"
Blog = "https://learningwithcode.com"
```

The next section is critical. It tells *setuptools* which directories to search fo the project code, and which packages in those directories to include in the build. In this case, we only have one package but you might have more in a project. It also tells *setuptools* which directories to exclude from the build.

```
[tool.setuptools.packages.find]
where = ["src"]
include = ["usermapper*"]
exclude = ["tests", "docs"]
```

Finally, the [console scripts](https://setuptools.pypa.io/en/latest/userguide/entry_point.html#console-scripts) table sets the name that will run the package in the command-line interface. This replaces the need to have a *\_\_main\_\_.py* file in the package directory  but I want to keep it around, for now, until I get my tests working. The \_\_main\_\_.py file lets me run the package from the *usermapper/src* directory with the command `python -m usermapper`. It does not seem to hurt to leave it.

```
[project.scripts]
usermapper = "usermapper.usermapper:main"
```

Save the *pyproject.toml* file.

Delete *setup.py* and *requirements.txt* files. They are no longer needed.

The final project structure looks like:

```bash
usermapper
├── docs
│   └── config.yaml.example
├── LICENSE
├── pyproject.toml
├── README.md
├── src
│   └── usermapper
│       ├── __init__.py
│       ├── __main__.py
│       ├── mapperdata.py
│       └── usermapper.py
└── tests
    ├── config.yaml
    ├── test.py
    └── user-mapping.xml.example
```

## Build the package

The project is currently a *[source distribution](https://packaging.python.org/en/latest/glossary/#term-Source-Distribution-or-sdist)* and can be installed as-is from my GitHub repository. To install it from PyPI, it needs to be converted into a *[distribution package](https://packaging.python.org/en/latest/glossary/#term-Distribution-Package)*

To create the distribution package, first create a new Python virtual environment so you can install the *wheel* and *build* packages:

```
$ python3 -m venv .bld
$ source .venv/bin/activate
(.venv) $ pip install wheel
(.venv) $ pip install build
```

In the same directory where *pyproject.toml* is located, run the *build* module: 

```
(.bld) $ python3 -m build
Successfully built usermapper-0.3.tar.gz and usermapper-0.3-py3-none-any.whl
```

See a new directory called *dist* in your project. It contains the two distributions:

```
dist
│   ├── usermapper-0.3-py3-none-any.whl
│   └── usermapper-0.3.tar.gz
```

You I now deactivate the build virtual environment and delete it (because its name is not in my *.gitignore* file):

```
(.bld) $ deactivate
$ rm -r .bld
```

## Test the packaged program

I tested the new package by installing it from the wheel I just created:

```
$ cd dist
$ python3 -m venv .bld
(.bld) $ source .venv/bin/activate
(.bld) $ python3 -m pip install usermapper-0.3-py3-none-any.whl
```

I test the installed program program using my *config.yaml.example* file as the config file:

```
(.bld) $ usermapper -i ../docs/config.yaml.example
```

A new file was created called *user-mapping.xml* in the same directory and it looked the way I expected it to look, so the test was a success.

Also, I ran the *test.py* program in the *tests* directory, which tests that the *usermapper* module can be imported and used in another program:

```
cd ../tests
python3 -m test
```

In this case, there is a *config.yaml* file in the *tests* directory and so it is used by default. Again, the program ran without errors and output a *user-mapping.xml* file.

When I ran a *diff* of the new *user-mapping.xml* file and *user-mapping.xml.example*, I saw see that only the lines containing the random passwords are different between the files. So, the test passed.

I plan to build better tests and continuous integration scripts in the future.

## commit changes to Git

After testing my changes to the package structure, committed the changes to my Git repository and merged the *repack* branch into the *main* branch.

```
$ git add -A
$ git commit -m "repackaged with modern tools"
$ git checkout main
$ git merge repack
$ git push origin
```

As an extra check, I tested that the package can be installed from the source distribution on Github because this is how my *usermapper-web* program, the web app that uses the *usermapper* package, installs it.

```
$ python3 -m venv .gittest
$ source .gittest/bin/activate
(.gittest) $ pip install git+https://github.com/blinklet/usermapper.git@v0.3
```

The install worked and a quick test shows that the module is available. So, I will not break any downstream apps that rely on the *usermapper* package's source distribution on GitHub.

When testing an install from a Git source distribution, you [may need to use](https://stackoverflow.com/questions/35898734/pip-installs-packages-successfully-but-executables-not-found-from-command-line) the `python3 -m usermapper` command instead of just `usermapper`.


## Configure *twine*

This time, I decided to publish my *usermapper* package to PyPI. I [created a new PyPI account](https://pypi.org/account/register/). I created a new username and password and I configured [two-factor authentication](https://blog.pypi.org/posts/2023-05-25-securing-pypi-with-2fa/).

Then, I configured *twine*. I installed it in my Python virtual environment"

```
$ python -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install wheel build
(.venv) $ python -m build
(.venv) $ pip install twine
```


In order to easily upload packages to PyPI, I got a [token]((https://pypi.org/help/#apitoken)) from PyPI that I can use to authenticate future uploads. To get the token, I went to my [PyPI Account Settings page](https://pypi.org/manage/account/) and scrolled down to the *API Tokens* section. Click the *Add API Token* button.

![Add an API token]({attach}pypi-new-token-030.png)

I gave the token a name and selected the token scope. 

![configure the token]({attach}pypi-new-token-040.png)

I copied the token and saved it to my secure password manager.

![copy the token]({attach}pypi-new-token-050.png)

I created a *PyPI* configuration file named *.pypirc* in my home directory and added the token to it.

```
(.venv) $ nano ~/.pypirc
```

I configured the *.pypirc* file, using my own token, similar to as shown below (with a fake token):

```
[pypi]
  username = __token__
  password = pypi-Wd94fakeNr2jvl3LnqfpOOnvfakeO0iEU8LTmWY6ovrEun5Uq3fakeOUmnwX
```

## Upload package to PyPI

I used *twine* to upload the *usermapper* package to PyPI.

```
(.venv) $ twine upload dist/*
```
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading usermapper-0.3-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 24.6/24.6 kB • 00:05 • 46.1 MB/s
Uploading usermapper-0.3.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 24.2/24.2 kB • 00:00 • 63.6 MB/s

View at:
https://pypi.org/project/usermapper/0.3/
```

I viewed the package on PyPI:

```
https://pypi.org/project/usermapper/0.3/
```

![PyPI project page]({attach}pypi-project-uploaded-060.png)

It took the *README.md* file from my Python project directory and displayed it. I need to make a few edits to the file now that my package is on PyPI, but that can wait until another time.
 
## Test the package works

```
$ (.venv) pip install usermapper
```

It installed correctly and I was able to test it. Everything worked.

And, it runs no matter where I am in my account. I do not need to type *python3 -m usermapper* to run it.

## Next steps

[tox](https://tox.wiki/en/latest/user_guide.html#basic-example) is an integrated build and test tool. It's not needed specifically for packaging, but is useful for building a basic continuous integration (CI) pipeline that supports testing your Python package. 





Use test.pypi.org
```
(.venv) $ pip install -i https://test.pypi.org/simple/ usermapper
```
```
Looking in indexes: https://test.pypi.org/simple/
Collecting usermapper
  Downloading https://test-files.pythonhosted.org/packages/56/9f/2351f4223517b686c0c9d2a75826fdc0f00bfa62d3b8cc35976f1aaea875/usermapper-0.3-py3-none-any.whl (17 kB)
Collecting PyYAML
  Downloading https://test-files.pythonhosted.org/packages/3a/09/50cff727ed4679924f3994c69a1fa27405a69a40038dc71b47204746ad2d/PyYAML-3.11.tar.gz (138 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 138.4/138.4 KB 2.4 MB/s eta 0:00:00
  Preparing metadata (setup.py) ... error
  error: subprocess-exited-with-error

  × python setup.py egg_info did not run successfully.
  │ exit code: 1
  ╰─> [7 lines of output]
      running egg_info
      creating /tmp/pip-pip-egg-info-9qtmf_7y/PyYAML.egg-info
      writing /tmp/pip-pip-egg-info-9qtmf_7y/PyYAML.egg-info/PKG-INFO
      writing dependency_links to /tmp/pip-pip-egg-info-9qtmf_7y/PyYAML.egg-info/dependency_links.txt
      writing top-level names to /tmp/pip-pip-egg-info-9qtmf_7y/PyYAML.egg-info/top_level.txt
      writing manifest file '/tmp/pip-pip-egg-info-9qtmf_7y/PyYAML.egg-info/SOURCES.txt'
      error: package directory 'lib3/yaml' does not exist
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.

note: This is an issue with the package mentioned above, not pip.
hint: See above for details.
```

Why this issue with test .pypi????

https://stackoverflow.com/questions/34514703/pip-install-from-pypi-works-but-from-testpypi-fails-cannot-find-requirements

"If you want to allow pip to also download packages from PyPI, you can specify --extra-index-url to point to PyPI. This is useful when the package you’re testing has dependencies:" See:
https://packaging.python.org/en/latest/guides/using-testpypi/





Add https://pypi.org/project/setuptools-scm/ to the pyproject.toml file so I can dynamically get the version number from the Git repo. 