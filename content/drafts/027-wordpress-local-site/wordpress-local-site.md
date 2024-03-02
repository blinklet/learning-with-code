title: Install and run a machine learning model on your laptop
slug: llm-laptop-ollama
summary: Discover how to run machine learning models, such as large language models, on consumer-grade computers using the Ollama project.
date: 2023-12-18
modified: 2023-12-18
category: Machine Learning
<!--status: Published-->

<!--
A bit of extra CSS code to center all images in the post
-->
<style>
img
{
    display:block; 
    float:none; 
    margin-left:auto;
    margin-right:auto;
}
</style>

This post describes how to use Docker containers to create a Wordpress server on your local PC and restore your Wordpress backup files to create a local copy of your site.

## Why create a local copy of Wordpress?

If you are reading this, you probably run a [Wordpress](https://wordpress.org/) server on a hosting provider, like [wordpress.com](https://wordpress.com/) or [BlueHost](https://www.bluehost.com/wordpress/wordpress-hosting), because you are not, and do not want to become, a Wordpress expert. You just want to create a useful content on a professional-looking blog. Your hosting provider handles all the complexity of deploying, securing, and managing a Wordpress site on the Internet.

You may, instead, want to build a local copy of your Wordpress site on your PC. In addition to acting as a [staging site](https://www.bluehost.com/help/article/wordpress-how-to-create-a-staging-site), a local Wordpress instance enables you to test restoring your Wordpress backup files and how your site will operate on different versions of server software.

### My problems

I wrote this post after [my other blog](https://www.brianlinkletter.com), which is a hosted Wordpess blog, stopped working due to a server error. [Jetpack Downtime Monitoring](https://jetpack.com/support/monitor/) did not detect the issue so I did not receive any alerts. My blog was down for over a week before I realized it.

The problem was caused when my service provide upgraded the software that supported my hosted Wordpress server. After my service provider resolved the issue, I decided to investigate if there were any more potential problems waiting to impact my blog. 

In my case, I needed to check the following:

* Do my Wordpress backups work? Can I restore my blog to another server if I have to?
* Is my Wordpress theme, which is old and no longer supported by its author, supported by later versions of PHP?
* Are the plugins I currently run supported by the newest version of PHP?

The simplest way to test these issues is to use Docker containers to deploy a Wordpress server and a database server on my local PC. 


Docker works on all major operating systems and makes it easy to run complex server software without having to learn how to install and configure it.

## Prerequisites

To create a local copy of your Wordpress site on your PC, you need to already have the following available to you:

* Access to the Wordpress dashboard on your hosted site. This is available at the *wp-admin* page on your site's domain. For example: `https://yoursite.com/wp-admin`.
* Backup files for your site. You need to generate these using a Wordpress plugin. I use the [UpdraftPlus](https://updraftplus.com/) backup plugin, which works well and has a free tier of service.
* Optionally, you may have a remote site to which your backup files are copied. I use [DropBox](https://www.dropbox.com) and I configured UpDraftPlus to automatically copy my backups to it.
* [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/) must be installed on your operating system. Follow the [Docker documentation](https://docs.docker.com/) to install these tools on your PC and to learn more about Docker.

## Create a local Wordpress instance

To create a simple Wordpress instance, follow the steps described below:

* Create a Docker compose file named *docker-compose.yml*.
* Run the `docker compose` command while in the same directory as the *docker-compose.yml* file.
* Connect to the Wordpress server running in its container and complete the Wordpress install.

### Create the *docker-compose.yml* file

First, create a new directory in which you will create the docker compose file. I named my directory *wordpress*.

```bash
$ mkdir wordpress
$ cd wordpress
```

Use your favorite text editor to create a Docker Compose file in the new directory:

```bash
$ nano docker-compose.yml
```

Enter the following text [^1] into the file:

[^1]: The original version of this file is on the [developer.wordpress.com blog](https://developer.wordpress.com/) at the following URL: [https://developer.wordpress.com/2022/11/14/seetup-local-development-environment-for-wordpress/](https://developer.wordpress.com/2022/11/14/seetup-local-development-environment-for-wordpress/)

```yaml
version: "1.0"
services:
 wordpress:
   image: wordpress:latest
   container_name: wordpress
   volumes:
     - html:/var/www/html
   environment:
     - WORDPRESS_DB_NAME=wordpress
     - WORDPRESS_TABLE_PREFIX=wp_
     - WORDPRESS_DB_HOST=db
     - WORDPRESS_DB_USER=root
     - WORDPRESS_DB_PASSWORD=password
     - WORDPRESS_DEBUG=1
   depends_on:
     - db
   restart: always
   ports:
     - 8080:80
 
 db:
   image: mariadb:latest
   container_name: db
   volumes:
     - db_data:/var/lib/mysql
   environment:
     - MYSQL_ROOT_PASSWORD=password
     - MYSQL_USER=root
     - MYSQL_PASSWORD=password
     - MYSQL_DATABASE=wordpress
   restart: always
 
volumes:
 html:
 db_data:
```

Save the *docker-compose.yml* file. 

This Docker Compose file defined two services named *wordpress* and *db*, and two volumes named *html* and *db_data*. It defines the containers, the  container images that each container will use from [Docker Hub](https://hub.docker.com/), the Docker volume each container will use, and the environment variables to be configured in each container when it starts. You can see that the HTTP port on the *wordpress* container will be mapped to TCP port 8080 on the local PC.

### Run *docker compose*

Run the `docker compose up -d` command to start the two containers. Docker will automatically create a network that connects the two containers together and to the *localhost* IP address on your PC. The `-d` or `--detach` option tells Docker to start the containers in detached mode which lets you use the terminal after the containers start.

```bash
$ docker compose up --detach
```

You will see output similar to the following as Docker downloads the specified images and starts the containers and the network:

```text
[+] Running 31/2
 ✔ wordpress 21 layers [⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿]      0B/0B      Pulled    102.5s 
 ✔ db 8 layers [⣿⣿⣿⣿⣿⣿⣿⣿]      0B/0B      Pulled                          92.9s 
[+] Running 3/3
 ✔ Network wordpress_default  Created                                      0.1s 
 ✔ Container db               Started                                      0.8s 
 ✔ Container wordpress        Started  
```

You can verify that the containers are running with the following command:

```text
$ docker ps
CONTAINER ID   IMAGE              COMMAND                  CREATED              STATUS              PORTS                                   NAMES
c6845d07b681   wordpress:php7.4   "docker-entrypoint.s…"   About a minute ago   Up About a minute   0.0.0.0:8080->80/tcp, :::8080->80/tcp   wordpress
15916e9cbb0d   mariadb:latest     "docker-entrypoint.s…"   About a minute ago   Up About a minute   3306/tcp  
```

And check that the volumes are created with the following command:

```text
$ docker volume ls
DRIVER    VOLUME NAME
local     wordpress_db_data
local     wordpress_html
```

## Install Wordpress

Start your favorite web browser and navigate to your local Wordpress server at the *localhost* address on your PC. Remember, it is available on *port 8080*. So, the URL is:

```text
http://localhost:8080
```

This opens the Wordpress installation page in the Browser.

![Wordpress install start page]({attach}000-wp-install.png){width=90%}

Follow the installation steps. Select your language and click the *Continue* button. The browser will display a form requesting site information. This will all eventually be replaced by the site information from the copied hosted Wordpress site, so just use some temporary information in this form.

![Wordpress account configuration]({attach}001-wp-install.png){width=90%}

Then, click on the *Install Wordpress* button. The next page asks you to log in. Click the *Log In* button to proceed.

![Wordpress install complete]({attach}002-wp-install.png){width=90%}

The browser display the Wordpress administration login page. 

![Wordpress wp-admin login page]({attach}003-wp-install.png){width=90%}

Use the userid and password you configured on the previous page and click the *Log In* button. Then, you will see the Wordpress Dashboard:

![Wordpress wp-admin dashboard]({attach}0034-wp-install.png){width=90%}

Open another browser tab and navigate to the local website URL again:

```text
http://localhost:8080
```

You should see a sample page using the Wordpress default theme.

![Wordpress sample page]({attach}005-wp-install.png){width=90%}

Wordpress is now running on your local PC. The next step is to copy your hosted Wordpress site to your local Wordpress server.

## Restore backup to local server

There are a couple of ways to transfer data from one Wordpress site to another. You could [export an XML file](https://wordpress.com/support/export/) from the first site and import it to the other site. Or, you could use a back up plugin to create a backup of your first site and then restore those backup files to the second site. We will use the backup procedure.

To restore backup files to the local Wordpress server, you must first install the same backup plugin on the local server as you were using on the remote server. I used *UpdraftPlus*, but the procedure should be similar if you used a different backup plugin.

First, install the plugin. In the Wordpress Dashboard, select *Plugins* in the sidebar menu and then select *Add New Plugin*. Search for your plugin and install it by clicking its *Install* button.

![Install backup plugin]({attach}006-install-plugin.png){width=90%}

The plugin should be installed. Next, click the *Activate* button on the plugin to activate it. Alternatively, you can activate the plugin from the *Plugins* menu item in the sidebar.

> **Troubleshooting tip:** If, when installing a plugin or trying to import a local file, Wordpress tries to start an FTP session, you need to modify one of the configuration files to make Wordpress use local files.
>
> First, you need to install an editor in the Wordpress container. Run the following commands:
>
>    $ docker exec -it wordpress apt update
>    $ docker exec -it wordpress apt install nano
>
> Edit the */var/www/html/wp-config.php* file in the Wordpress container. 
> 
>    $ docker exec -it wordpress nano /var/www/html/wp-config.php
>
> Add the following text after the last line in the file:
>
>    define('FS_METHOD', 'direct');
>
> If you are using *nano*, press *CTRL-X* to save the file and exit. This should stop the unwanted FTP dialog from appearing in the future.

Go to the UpdraftPlus plugin settings. Either click on the menu *Plugins --> Installed Plugins* and then select the *Settings* link in the UpdraftPlus plugin, or click on *Settings --> UpdraftPlus Backups*.

![Go to plugin settings]({attach}007-install-plugin.png){width=90%}

In the *UpdraftPlus Backup* settings, click on the *Settings* tab. Then, click on the storage provide that is hosting the backup files generated by your remote Wordpress site. In my case, I use DropBox so I selected it from the list. Click the *Save Changes* button in the top right corner:

![Select backup file location]({attach}008-set-up-restore.png){width=90%}


Click on link

![Click on link]({attach}009-set-up-restore.png){width=90%}

Click on *Complete setup* button

![Complete setup]({attach}010-set-up-restore.png){width=90%}

Log into dropbox

Click Rescan remote

![Scan storage]({attach}011-scan-storage.png){width=90%}

In list of valid backups, pick most recent one

![Select backup to restore]({attach}012-restore.png){width=90%}

Select all the file, then click *Next*.

![Select files to restore]({attach}013-restore.png){width=90%}


![Downloading files]({attach}014-restore.png){width=90%}

you might see some warnings. Figure out how to respond. In my case, I just accepted Updraft's recommended solution.

Also, be sure to check the box: *Search and replace site location in the database (migrate)*. Click *Restore*.

![Migrate database]({attach}015-restore.png){width=90%}

Restore succesful. Click on *Return to UpdraftPlus configuration* button.

![Migrate database]({attach}016-restore.png){width=90%}


# potential problems and solutions

looks like an old plugin names "word stats" (9 years since an update) is not compatible with PHP8.2. (Removed now from remote siote)

Civil Footnotes is also at risk

Also, Standard theme is incompatible.

after installing everything except themes all at once

```
Fatal error: Uncaught Error: Non-static method Word_Stats_Core::load_options() cannot be called statically in /var/www/html/wp-content/plugins/word-stats/word-stats.php:46 Stack trace: #0 /var/www/html/wp-settings.php(473): include_once() #1 /var/www/html/wp-config.php(133): require_once('/var/www/html/w...') #2 /var/www/html/wp-load.php(50): require_once('/var/www/html/w...') #3 /var/www/html/wp-admin/admin.php(34): require_once('/var/www/html/w...') #4 /var/www/html/wp-admin/options-general.php(10): require_once('/var/www/html/w...') #5 {main} thrown in /var/www/html/wp-content/plugins/word-stats/word-stats.php on line 46 Notice: Function is_embed was called incorrectly. Conditional query tags do not work before the query is run. Before then, they always return false. Please see Debugging in WordPress for more information. (This message was added in version 3.1.0.) in /var/www/html/wp-includes/functions.php on line 6031 Notice: Function is_search was called incorrectly. Conditional query tags do not work before the query is run. Before then, they always return false. Please see Debugging in WordPress for more information. (This message was added in version 3.1.0.) in /var/www/html/wp-includes/functions.php on line 6031

There has been a critical error on this website. Please check your site admin email inbox for instructions.

Learn more about troubleshooting WordPress.
```

after installing items one at a time after logging into to site after database

```
Fatal error: Declaration of Standard_Nav_Walker::start_lvl(&$output, $depth, $args) must be compatible with Walker_Nav_Menu::start_lvl(&$output, $depth = 0, $args = null) in /var/www/html/wp-content/themes/Archive/lib/Standard_Nav_Walker.class.php on line 12

There has been a critical error on this website. Please check your site admin email inbox for instructions.

Learn more about troubleshooting WordPress.
```



In my case, Wordpress encountered a PHP error when it returned to the site and started it. Either the *Standard* theme is not compatible with wordpress. The solution is to start again but do not download the themes or plugins.

To restore back to nothing:

```
$ docker compose down
$ docker volume rm wordpress_db_data
$ docker volume rm wordpress_html 
$ docker compose up --detach
```



![Pick fewer items to restore]({attach}013b-restore.png){width=90%}

After restore successful, return to updraftplus configuration asks for login. Use useid and password from the remote site, because it was part of the database that was restored.

![Login to new site]({attach}017-login-works.png){width=90%}
















# Error

Looks like plugins or something not compatible with PHP 8.2. Get old container with PHP 7.4???


docker pull wordpress:php7.4
wordpressdevelop/php:7.4-fpm

Or, downgrade PHP on the latest wordpress   

* https://linux.how2shout.com/how-to-install-php-7-4-on-ubuntu-22-04-lts-jammy-linux/
* https://webdock.io/en/docs/perfect-server-stacks/upgrade-or-downgrade-php/upgrading-or-downgrading-php-versions

```
$ docker exec -it wordpress bash
# apt update
# apt install software-properties-common
# apt install python3-launchpadlib
# add-apt-repository ppa:ondrej/php -y
# apt update
# apt install php7.4
# apt install php7.4-{cli,common,curl,zip,gd,mysql,xml,mbstring,json,intl}
# update-alternatives --config php
```

# clear volume

To start over: must also delete the docker volume *wordpress_db_data*

```
$ docker volume ls
$ docker volume rm wordpress_db_data
```

# The Standard Theme is the problem!!!

If I activate the standard theme, the web site fails. It seems to be incompatible with PHP 8.2. As soon as Bluehost updates their servers to Ubuntu 22 or 24, I am toast!!! (PHP 8.x is in Ubuntu 22 and 24)

https://support.rebel.com/hc/en-us/articles/360047782954-How-do-I-fix-a-WordPress-website-broken-by-a-PHP-upgrade-Classic-Hosting




Setting Up a New WordPress Instance with Docker:

    Provide a concise step-by-step guide on using Docker to create a new WordPress instance.
    Include code snippets or commands for creating Docker containers for WordPress and MySQL.

Exporting Your Data from the Hosted Site:

    Guide on how to use the WordPress export tool to download site data (posts, pages, comments, media files).
    Mention any additional steps for exporting plugin settings or custom configurations if applicable.

Importing Data into Your Local WordPress:

    Instructions on accessing the local WordPress dashboard to import the previously exported data.
    Tips for ensuring all media files and links are correctly imported and functioning.

Mirroring Your Hosted Environment:

    Advice on how to install and activate the same themes and plugins on the local copy to ensure consistency.
    Suggest using the same versions to avoid compatibility issues.

Troubleshooting Common Issues:

    Address common problems users may encounter, such as import errors, plugin or theme incompatibilities, and Docker container configuration issues.
    Offer solutions or workarounds for these issues.

Potential Challenges and Their Resolutions:

    Discuss potential challenges in more depth, including database connection errors, file permissions, and URL mismatches.
    Provide expert advice on resolving these challenges to ensure a smooth transition.

Maintaining Your Local Environment:

    Offer tips for keeping the local WordPress installation up to date with the hosted site.
    Suggest practices for regular backups and testing of new updates or changes locally before applying them to the live site.

Conclusion:

    Encourage readers to explore further Docker functionalities and WordPress development practices.
    Remind them of the value of a local development environment for experimentation and learning.