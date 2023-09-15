title: Packaging Python applications using modern tools
slug: python-packaging-modern
summary: Python packaging has changed over the past few years. In this post, I will update the way my *usermapper* Python package is structured and use modern tools to re-publish it.
date: 2023-09-30
modified: 2023-09-30
category: Python
<!-- status: Published -->

To distribute your Python program so it can be installed using a package manager like *[pip](https://pip.pypa.io/en/stable/)* or *[pipx](https://github.com/pypa/pipx)*, you need to package it. The [Python packaging process](https://packaging.python.org/en/latest/) has [evolved](https://drivendata.co/blog/python-packaging-2023) since I covered my [first experience packaging a Python application]({filename}/articles/005-install-package-cli-program-pipx/install-package-cli-program-pipx.md) several years ago. In this post, I will revisit my *[usermapper]({filename}/articles/002-python-learning-network-engineers/python-learning-network-engineers.md)* project and re-package it using the modern Python packaging process.

## The modern Python packaging tools

The [Python Packaging Authority](https://www.pypa.io/en/latest/) (PyPA) [recommends](https://packaging.python.org/en/latest/guides/tool-recommendations/#packaging-tool-recommendations) the following packaging tools:

* *[pip-tools](https://github.com/jazzband/pip-tools)* contains the *pip-compile*  and *pip-sync* tools that help you manage dependencies in your Python package.
* *[setuptools](https://setuptools.pypa.io/en/latest/)* is the recommended "backend" for the Python package creation process
* *[build](https://pypa-build.readthedocs.io/en/stable/index.html)* provides the "frontend" for the Python package creation process.
* *[twine](https://twine.readthedocs.io/en/latest/)* uploads packages to the PyPI database so they can easily be distributed.

There are [many alternative packaging tools](https://packaging.python.org/en/latest/key_projects/#project-summaries) available. The other tools all offer additional functionality and some of them automate part of the packaging and distribution process. The Python community does not seem to agree on which is the best tool for most cases. I will start with the basics and use the tools recommended by the PyPA.

All of the modern packaging tools use the *[pyproject.toml](https://peps.python.org/pep-0621/)* file in your Python project's directory.


## Project organization

I cloned the project to my PC from my GitHub repository:

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

Start working on a new git branch:

```bash
$ cd usermapper
$ git branch repack
$ git checkout repack
```
I re-organized Python files in my project directory according to the [recommendations](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#src-layout) made by the *setuptools* project team:

* I added a *docs* folder so that I can add [project documentation](https://packaging.python.org/en/latest/tutorials/creating-documentation/) in the future. The *config.yaml.example* file serves as partial documentation, for now.
* I added a *src* folder and moved the *usermapper* package into it. 
* I added *tests* directory and moved the *tests.py* file into it. This is a very basic test script. In the future, after I learn more about adding unit and system tests to Python projects, this directory will contain all the test code. 

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

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

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

[tool.setuptools.packages.find]
where = ["src"]
include = ["usermapper*"]
exclude = ["tests", "docs"]

[project.scripts]
usermapper = "usermapper.usermapper:main"
```

https://packaging.python.org/en/latest/specifications/core-metadata/#project-url-multiple-use

console script eliminates need for __main__.py in package   https://setuptools.pypa.io/en/latest/userguide/entry_point.html#console-scripts


Then delete *setup.py* and *requirements.txt*. They are no longer needed.

The file *src/usermapper/__main__.py* is no longer needed to run the installed program but I want to keep it around, for now, until I get my tests working. The __main__.py file lets me run the package from the *usermapper/src* directory with the command `python -m usermapper`. 

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

https://packaging.python.org/en/latest/tutorials/packaging-projects/

The project is currently a "source package". To install it via pip, it needs to be converted into a "dist

```
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install wheel
(.venv) $ pip install build
```

In the same directory where *pyproject.toml* is located: 

```
(.venv) $ python3 -m build
Successfully built usermapper-0.3.tar.gz and usermapper-0.3-py3-none-any.whl
```

See a new directory called *dist* in your project. It contains the two distributions:

```
dist
│   ├── usermapper-0.3-py3-none-any.whl
│   └── usermapper-0.3.tar.gz
```


## Test

Install the wheel

```
cd dist
python3 -m pip install usermapper-0.3-py3-none-any.whl
```

test the installed program

```
cd ../docs
usermapper -i config.yaml.example
```

A new file should be created called *user-mapping.xml* in the same directory.

Also, run the test.py program in the *tests* directory

cd ../tests
python3 -m test

again, the program should run without errors and output a user-mapping.xml file.

If you run a *diff* of the new *user-mapping.xml* file and *user-mapping.xml.example*, you should see that only the lines containing the random passwords are different between the files.


Note that deleting the __main__.py file means that, to test the program, I need to package it and then install it with pip. Maybe I should leave it there


## commit changes to Git

git add -A
git commit -m "repackaged with modern tools"
git checkout main
git merge repack
git push origin


## Next steps

[tox](https://tox.wiki/en/latest/user_guide.html#basic-example) is an integrated build and test tool. It's not needed specifically for packaging, but is useful for building a basic continuous integration (CI) pipeline that supports testing your Python package. 