title: Host your Pelican Static Web Site on Cloudflare Pages
slug: host-static-web-site
summary: How to deploy your Pelican static web site to Cloudflare Pages using their GitHub integration
date: 2022-10-05
modified: 2022-10-05
category: Blogging
status: published

I decided to use [Cloudflare Pages](https://pages.cloudflare.com/) to host static my web site. It offers a [free service tier](https://pages.cloudflare.com/#pricing) that supports my needs and has all the features I need. This post describes how to deploy your Pelican site to Cloudflare Pages.

To [deploy an existing Pelican static web site to Cloudflare Pages](https://developers.cloudflare.com/pages/framework-guides/deploy-a-pelican-site/), you must use their [Git integration](https://developers.cloudflare.com/pages/platform/git-integration/) so you need a [GitHub](https://github.com/) account in addition to a Cloudflare account. The steps I recommend you follow to deploy your blog to Cloudflare Pages are:

1. Create the *requirements.txt* file required by Cloudflare Pages
2. Copy the theme directory to your blog directory so it can be  included in the files sent to Cloudflare Pages
3. Create a Git repository for your project and sync it with your GitHub account
4. Set up a Cloudflare account
5. Create a new Cloudflare Pages project and connect it to your blog's GitHub repository
6. Deploy your site to Cloudflare Pages and test it

## The starting point

I assume you have already created a Pelican blog and have built and tested it on your local PC. This example uses the project directory I created for my blog. The current example directory structure, with files, is:

```bash
learning_with_code
├── content
│   ├── extras
│   ├── images
│   │   └── image-test-post
│   │       └── image.png
│   ├── image-test.md
│   └── this-is-a-test-post.md
├── output
├── pelicanconf.py
├── publishconf.py
└── env
```

I also assume you are familiar with using [Git](https://git-scm.com/) and GitHub.

## Add a *requirements.txt* file

According to [Cloudflare's documentation about setting up a Pelican site](https://developers.cloudflare.com/pages/framework-guides/deploy-a-pelican-site/), Cloudflare Pages requires a [*requirements.txt* file](https://realpython.com/lessons/using-requirement-files/) exist in the project directory. It uses this file every time it builds your static web site.

Create the file. First, ensure your virtual environment is activated:

```bash
$ source env/bin/activate
(env) $
```

Then run the `pip freeze` command to get the information you need for the *requirements.txt* file.

I found that Cloudflare Pages do not necessarily support the latest versions of the required Python packages so the versions you installed on your local PC may be newer than what Cloudflare Pages can support. To avoid this problem, generalize your requirements file by removing the package version numbers on each line.

On Linux or Max OS, create the requirements file with the command shown below:

```bash
(env) $ pip freeze | sed s/=.*// > requirements.txt
```

On Windows, the `sed` command is not available so just run the following command. Then, open the *requirements.txt* file in a text editor and delete the version information from each line. 

```powershell
(env) > pip freeze > requirements.txt 
```

The contents of the *requirements.txt* file should look similar to the following, but may include more packages if you also have Pelican plugins installed.

```
blinker
docutils
feedgenerator
Jinja2
Markdown
markdown-it-py
MarkupSafe
mdurl
pelican
Pygments
python-dateutil
pytz
rich
six
Unidecode
```

If you add more Pelican plugins or other Python packages that support your blog, you must run the freeze command again to rebuild the *requirements.txt* file.


## Copy the theme directory to your blog directory

There are multiple places you can store your Pelican theme files. Most Pelican tutorials recommend you store your theme files outside your project directory. However, Cloudflare Pages needs access to your theme files. Since you are interfacing with Cloudflare pages via a GitHub integration, the theme files must be included in your Git repository.

That means the theme file should be in the blog's project directory. You will have to manually copy the theme to a folder to your project directory and update the *pelicanconf.py* file to point to the folder.

For example, I use the [Flex theme](https://github.com/alexandrevicenzi/Flex#flex). But, I previously had installed it using the *pelican-themes* tool so the files are all in my Python environment folder. To keep using the Flex theme when this blog is published to the Cloudflare Pages, I copied the theme files from my environment directory to my project directory. 

first, list the thems you have installed in verbose mode so you can see the directories in which they are stored.

```bash
(env) $ pelican-themes -lv
/home/brian/Projects/learning-with-code/env/lib/python3.10/site-packages/pelican/themes/notmyidea
/home/brian/Projects/learning-with-code/env/lib/python3.10/site-packages/pelican/themes/simple
/home/brian/Projects/learning-with-code/env/lib/python3.10/site-packages/pelican/themes/Flex-2.5.0
```

Then, create a new directory in your project called *themes* and copy the Flex-2.5.0 directory into it:

```bash
(env) $ mkdir themes
(env) $ cp /home/brian/Projects/learning-with-code/env/lib/python3.10/site-packages/pelican/themes/Flex-2.5.0 themes/
(env) $ ls -1
content
env
output
pelicanconf.py
publishconf.py
requirements.txt
themes
```

Then, I changed the `THEME` variable in your *pelicanconf.py* file to point to the relative path of the Flex theme directory:

```python
THEME = ./themes/Flex-2.5.0
```

I saved the *pelicanconf.py* file.

### Rewrite the *publishconf.py* settings file

You might someday use different settings to publish your blog. For example, you might enable RSS feeds on a published site but not on the local version of your site or you might allow draft posts to be visible on your local PC but not on the published site.

For now, rewrite the *publishconf.py* settings file so it just imports the settings from your *pelicanconf.py* settings file. You can add different variables to the *publishconf.py* file in the future, when you need to. 

Edit the *publishconf.py* file so it looks like the following below:

```python
import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *
```

You need to remember to set up Cloudflare to use the *publishconf.py* file instead of the default settings file when you set up your build command in a future step.

### Deactivate the Python environment

Optionally, you may then deactivate the virtual environment.

```bash
(env) $ deactivate
$
```

I just wanted to make it clear that, from this point on, we are not using Python.


## Create a Git repository and sync it with your GitHub account

I assume you have Git installed on your computer. If not, detailed installation instructions are on the Git web site at [https://git-scm.com](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

## Create a local Git repo

Your Pelican web site is in a project directory. For example, my directory is named *learning-with-code*.

```bash
$ cd learning-with-code
$ ls -1
content
env
output
pelicanconf.py
publishconf.py
requirements.txt
themes
```

Note that the Python virtual environment used to build the web site is in the project directory, in a subdirectory named *env*. That's the way I like to manage my Python virtual environments. You may organize your virtual environments differently.

Create a [new git repository](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup) in the directory. First, configure the name of the main branch and user information:

```bash
$ git config --global user.name "Brian Linkletter"
$ git config --global user.email fake@example.com
$ git config --global init.defaultBranch main
```

Add a [*.gitignore* file](https://git-scm.com/docs/gitignore) so you do not track the Python environment files and other Python infrastructure with the web site source code.

Get the *Python.gitignore* file from [GitHub's gitignore repository](https://github.com/github/gitignore). It comes with the *env/* directory already configured to be ignored.

```bash
$ wget https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore
$ mv Python.gitignore .gitignore
```

Then, add the *output* directory to the *.gitignore* file. You do not need to track the files generated by Pelican in your Git repository. You only need to track your source code.

Add the following lines to the end of the *.gitignore* file:

```bash
# Pelican framework files
output/
```

Save the file.

Initialize the Git repository 

```bash
$ git init
```

Add the existing web site files into the repository as your first commit

```bash
$ git add -A
$ git commit -m "testing first static web site"
```

Now you have a git repository that tracks all the source files that pelican uses to build your web site.

## Configure a *Git remote* on GitHub

Cloudflare Pages integrates with the GitHub platform. You need to create a remote repository on GitHub and sync your local Git repository with it.

I assume you have a GitHub account. If not, follow the instructions on the GitHub web site to [create your own GitHub account](https://docs.github.com/en/get-started/signing-up-for-github/signing-up-for-a-new-github-account).

I also assume you have provided your SSH public key to GitHub. If not, follow the instructions on *github.com* to [create and configure SSH authentication](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account).

Log into your GitHub account and [create a new repository](https://docs.github.com/en/get-started/quickstart/create-a-repo). In my case, I named the repository *learning-with-code*, the same name as my local project directory.

Do not create a *.gitignore* file because you already have one in your local repository. Click on the *Create repository* button.

### Sync your local repository with GitHub

Now, sync your local Git repository with the remote GitHub repository:

```bash
$ git remote add origin git@github.com:blinklet/learning-with-code.git
$ git branch -M main
$ git push -u origin main
```

## Cloudflare Pages setup

Create an account on Cloudflare. Go to [https://pages.cloudflare.com/](https://pages.cloudflare.com/) and click on *Sign Up*. Provide an e-mail address and choose a password and click on *Sign up*. Your account will be verified via e-mail.

### Enable Cloudflare GitHub integration 

Cloudflare offers good documentation that describes [how to deploy a Pelican site](https://developers.cloudflare.com/pages/framework-guides/deploy-a-pelican-site/). Below, I list a summary of the steps for your convenience:

1. In the Cloudflare dashboard, click on *Pages* then click on *Connect to Git*.
2. Choose *GitHub* and then click on *Connect GitHub*
3. Select *Only select repositories* and then choose your web site's repo. In my case, I chose "learning-with-code". Click on *Install & Authorize*
4. Back at the dashboard, click on the repository again so the *Begin setup* button lights up. The click on *Begin setup*

### Pages settings

In the next page, verify the web site name and make a note of the URL the web page will have. In this example, I set the project name to the name I want my website to have: "Learning-with-code". So, the URL will be [*https://learning-with-code.pages.dev*](https://learning-with-code.pages.dev).

Choose "Pelican" from the *Frameworks* menu. This automatically populated the *Build command* and *Build output directory* fields with default values. Leave the build output directory at the default value of "output".

#### Set the build command

Remember, You might someday use different settings to publish your blog so configure Cloudflare Pages to use the optional *publishconf.py* settings file when it builds the web site.

Change the build command to:

```bash
pelican content -s publishconf.py
```

### Set *PYTHON_VERSION* environment variable

On the same Settings page, add an environment variable that defines the version of Python that Cloudflare Pages will use. Cloudflare requires you set the *PYTHON_VERSION* environment variable to *3.7*. Click the *Save* button to set the variable.

I was surprised they only support a version of Python that is so old but I tried new versions and they did not work.

## Deploy

Finally, click *Save and Deploy* at the bottom of the page to complete the setup.

From this point on, Cloudflare will watch your GitHub repository and will re-build and re-deploy the web site every time you push any changes up to the Github repository.

### Test your blog

Check the build status of your deployment on Cloudflare Pages. You will see any errors, if they occurred.

Make an update to your blog on your local PC. For example, create a new post or just add a dummy file to the *extras* directory. Then, push the change to GitHub. In my case, the commands I would enter are:

```bash
$ cd learning-with-code
$ git add -A
$ git commit -m "testing deployment"
$ git push
```

Cloudflare Pages will detect that a change has occurred in your GitHub repository and automatically download the changed files and re-build your web site using the new files.

In the Cloudflare Pages dashboard, click on *Workers and Pages* in the left-side menu. Here you will see all your projects and information about each one, including the URL of the web site. 

Click on the name of your project. On the next page, you will see the status of your deployment and you can click on *View details* to see the build status messages. If you see any errors, the error messages will help you debug the problem.

Test your web site by entering its URL into your browser. In my case, I opened the URL: [https://learning-with-code.pages.dev/](https://learning-with-code.pages.dev/)

# Conclusion

Now, your static web site is set up and ready to serve.

In a future post, I will discuss [how to set up a custom domain]({filename}add-custom-domain-to-cloudflare-pages.md) so you can use a domain name of your choice, instead of the domain *pages.dev*.

