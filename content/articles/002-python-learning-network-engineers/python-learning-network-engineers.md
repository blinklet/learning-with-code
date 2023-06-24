title: Video Learning Path for Python Programming
slug: python-learning-network-engineer
summary: A set of ten videos I created, along with links to learning resources associated with each video's topic, that work through all the steps required to build a useful network automation Python program and share it with others.
date: 2020-11-30
modified: 2020-11-30
category: Python
status: published

<!--
A bit of extra CSS code to make all embedded video 
frames centered in the post
-->
<style>
iframe
{
    display:block; 
    float:none; 
    margin-left:auto;
    margin-right:auto;
}
</style>

I recorded videos as I learned and practiced Python programming. I think these videos, along with the links to learning resources associated with each video's topic, serve as a good learning guide for network engineers getting started with Python programming.

This post collects links to all ten videos I created. Over the course of these videos, I wrote a program called *Usermapper* that reads a configuration file and builds an [XML authentication file for the Guacamole web proxy](https://guacamole.apache.org/doc/gug/configuring-guacamole.html#basic-auth). I also used the Git version control system and packaged the code on my [Usermapper GitHub repository](https://github.com/blinklet/usermapper)

## Topics I need to learn

I learned some programming during my Electrical Engineering degree program many years ago. After I graduated, except for some basic scripting, I've not had to do any programming.

<iframe width="560" height="315" src="https://www.youtube.com/embed/q7SmsE44cIo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

These videos do not cover the basics of Python. I strongly suggest you read a book about Python, or watch some video training (see suggestions below) before you start working through these videos. Before I started recording this first video, I read the O'Reilly book, *Learning Python*, and wrote a [blog post]({filename}/articles/001-python-minimum-you-need-to-know/python-minimum-you-need-to-know.md) about what I learned in the first part of the book.

This video refers to the following resources:

* [The Learning Python book, by Mark Lutz](https://learning-python.com/about-lp5e.html)
* [Microsoft's Introduction to Python Development videos](https://channel9.msdn.com/Series/Intro-to-Python-Development)
* [Microsoft's More Python for Beginners videos](https://channel9.msdn.com/Series/More-Python-for-Beginners)
* [A Python style guide](https://docs.python-guide.org/writing/style/)

## My first Python program

In this video, I write the first part of a program that will build a user authentication file that is compatible with the [Apache Guacamole web proxy server](https://guacamole.apache.org/). The output file will eventually be in XML format but this first version creates a Python dictionary populated with all the required information.

<iframe width="560" height="315" src="https://www.youtube.com/embed/Fgag8z9ZG4k" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

As I wrote this code, I learned more about the modules and packages available in [Python's standard library](https://docs.python.org/3/library/). I also got some good practice with the Python Object Model as it relates to copying opjects and references to objects. 

I mention the following resources in this video: 

* [Copying Python objects](https://realpython.com/copying-python-objects/)
* [Shallow copy vs Deep copy](https://stackoverflow.com/questions/3975376/understanding-dict-copy-shallow-or-deep)
* [The Python standard library](https://docs.python.org/3/library/).
* [The Guacamole default authentication file format ](https://guacamole.apache.org/doc/gug/configuring-guacamole.html#basic-auth)

## Writing an XML file

In my previous video, I created a nested dictionary containing the raw data that must be written, in XML format, to the user mapping file. In this video, I add the code that writes an XML file based on that dictionary's contents. I solve problems like parsing through several layers of a nested dictionary to modify values.

<iframe width="560" height="315" src="https://www.youtube.com/embed/tmvGEg89OnE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

I mention the following resources in this video: 

* [Iterating through a list of dictionaries ](https://stackoverflow.com/questions/35864007/python-3-5-iterate-through-a-list-of-dictionaries)
* [XML Overview ](https://www.w3schools.com/xml/default.asp)

## Reorganizing my program

<iframe width="560" height="315" src="https://www.youtube.com/embed/JkiXvgvf7_g" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

In this video, I'll explore a bit more about Python by organizing my current project into functions and modules to make it easier to maintain.

My project currently consists of one file and the data used to build the XML output file is hard-coded into the program. This is not very flexible and makes it hard for others to use the program. First I will divide the project into module files and then turn some of the program logic into functions.

I mention the following resources in this video: 

* The [Guacamole default authentication file format](https://guacamole.apache.org/doc/gug/configuring-guacamole.html#basic-auth)

## Git and GitHub

In this video, I use the Git version control system to manage changes to my code and also create a remote repository on Github.

<iframe width="560" height="315" src="https://www.youtube.com/embed/7EY_7Spb-Jg" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Before watching this video, I recommend you review the following:

* [Getting started with Git videos (20 minutes total)](https://git-scm.com/videos)
* [GitHub guides videos: The getting-started playlist](https://www.youtube.com/watch?v=noZnOSpcjYY&list=PLg7s6cbtAD15G8lNyoaYDuKZSKyJrgwB-)

Other resources I mention in this video are:

* [The git documentation](https://git-scm.com/doc)
* [Git cheat sheet](https://training.github.com/downloads/github-git-cheat-sheet.pdf)
* [GitHub First Contributions repo](https://github.com/firstcontributions/first-contributions)
* [Another good guide to using git](https://alan-turing-institute.github.io/rsd-engineeringcourse/ch02git/02Solo.html)

## Python virtual environments

In this video, I start making my first program more flexible. I define the input in a configuration file. I learn the YAML file format. I introduce Python virtual environments. Also, I get more practice using Git as I make my code changes. 

<iframe width="560" height="315" src="https://www.youtube.com/embed/ya4WUocyW7w" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Before watching this video, I recommend you review the following:

* [Python virtual environments overview](https://docs.python.org/3/tutorial/venv.html)

Other resources I mention in this video are:

* [YAML overview: ](https://en.wikipedia.org/wiki/YAML)
* [YAML web site](https://yaml.org)
* [Python package index (PyPI)](https://pypi.org/)



## Rewriting *mapperdata.py*

In this video, I continue making my first program more flexible. I use a Python virtual environment. I install the *PyYAML* package using pip. I rewrite my *mapperdata.py* module to read the YAML config file and build a data structure based on its contents. I make a few classic mistakes while iterating through nested dictionaries and I introduce the useful git restore command. 

<iframe width="560" height="315" src="https://www.youtube.com/embed/tOimWt7JiaY" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Before watching this video, I recommend you review the following:

* [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation)

Other resources I mention in this video are:

* [A better YAML overview](https://rollout.io/blog/yaml-tutorial-everything-you-need-get-started/)
* [Tool for testing yaml config file](http://www.yamllint.com/)
* [Generate random passwords](https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits)
* [Python secrets module](https://docs.python.org/3/library/secrets.html)

## Using VS Code

In this video, I finish rewriting my *mapperdata.py* module to read the YAML config file and build a data structure based on its contents. I also introduce the Visual Studio Code text editor, which I'll be using from now on. 

<iframe width="560" height="315" src="https://www.youtube.com/embed/ClrmLDNqf6M" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Before watching this video, I recommend you review the following short videos:

* [Configuring Visual Studio Code](https://channel9.msdn.com/Series/Intro-to-Python-Development/Python-for-Beginners-4-of-44-Configuring-Visual-Studio-Code)
* [Starting with VS Code](https://channel9.msdn.com/Series/Intro-to-Python-Development/Python-for-Beginners-6-of-44-Demo-Hello-World)

Other resources I mention in this video are:

* [How to install VS Code](https://code.visualstudio.com/docs/setup/linux)
* [VS Code](https://code.visualstudio.com/)
* [Python in VSCode](https://code.visualstudio.com/docs/languages/python)
* [Version control in VS Code](https://code.visualstudio.com/docs/editor/versioncontrol)
* [Git in VS Code](https://www.digitalocean.com/community/tutorials/how-to-use-git-integration-in-visual-studio-code)
* [VS Code crash course](https://www.youtube.com/watch?v=WPqXP_kLzpo)
* [Padding a string with zeros](https://stackoverflow.com/questions/39402795/how-to-pad-a-string-with-leading-zeros-in-python-3/39402910)


## *Requirements.txt* and using *GitHub Issues*

In this video, I create a *requirements.txt* file so others can easily deploy the Usermapper application. I also fix a bug I found in the program. I use GitHub Issues to save notes about improvements I would like to make to the application, if I find time in the future. Finally, I discuss what I think it will take to learn enough about the Flask framework so I can move on to the next step.

<iframe width="560" height="315" src="https://www.youtube.com/embed/xPNwKmpey5Y" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Resources I mention in this video are:

* [The Flask framework](https://flask.palletsprojects.com)

## Packaging and command-line arguments

In this video, I organize my Python modules into a package that others can download and install. I also modify the program so users can specify the input file and output file locations and filenames in command line arguments. The final result is at: [https://github.com/blinklet/usermapper.git](https://github.com/blinklet/usermapper.git)

<iframe width="560" height="315" src="https://www.youtube.com/embed/VxAe6tfjiPw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

Before watching this video, I recommend you read the following article:

* [Packaging Python programs](https://uoftcoders.github.io/studyGroup/lessons/python/packages/lesson/)

Other resources I mention in this video are:

* [Python module search paths (the -m option)](https://docs.python.org/3/using/cmdline.html)
* [The package setup.py file](https://docs.python.org/3/distutils/setupscript.html)
* [Command line arguments for Python programs](https://realpython.com/python-command-line-arguments/)
* [Why we need a module named \_\_main\_\_ in the package directory](https://docs.python.org/3/using/cmdline.html)
* [Install Python packages hosted on Github](https://pip.pypa.io/en/stable/reference/pip_install/#vcs-support)
* [References in GitHub](https://docs.github.com/en/free-pro-team@latest/github/writing-on-github/autolinked-references-and-urls)

## Conclusion

Over the course of a month, I spend about one hour per evening learning and practicing Python. I found that choosing a specific project to implement in Python helped me learn. If you administer a Guacamole web proxy server, have a look at my [Usermapper](https://github.com/blinklet/usermapper) program! I am now looking forward to learning the Flask framework and building a web site using Python.