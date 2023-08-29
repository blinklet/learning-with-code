title: Writing drafts for Pelican blogs
slug: writing-drafts
summary: Here are some tips for conveniently working on draft blog posts for your Pelican blog while keeping your work in progress from appearing on your published web site.
date: 2023-05-15
modified: 2023-05-15
category: Blogging
status: draft

(Maybe turn this into how I work in Pelican, in general)


When you work on a post for your Pelican-based blog, you probably don't want the draft post to appear on your published blog. But, that could happen if, while you are working on a draft for your next post, you re-deploy your blog. Here are some tips for conveniently working on draft blog posts for your Pelican blog while keeping your work in progress from appearing on your published web site.

this is a test of a draft image

![test image in draft]({attach}image-draft.png)

There are, of course, many ways to accomplish the same goal. Here are some of the ways you can ensure your work in progress does not get accidentally published to your blog.

First, organize your draft work

* Work in a draft folder. This is optional but I recommend it.

Next, set up Pelican so it is easy to test your drafts without accidentally publishing them. You may use one of three methods

1. Use *status: draft* metadata
2. Use default metadata
3. Work in a new branch


## Work in a draft folder

(replace text below with 

draft folder makes it easier to know what I am working on

BUT!!! does not solve the accidental publishing issue all by itself

include "images in draft folder"
)

The simplest method is to set up a folder outside your *content* directory that contains the Markdown file for your future post plus any other files you need like images. Edit the Markdown file and test the way the post will look using a Markdown preview feature in your text editor or a separate preview application.

Then, when it is time to publish the post, add the metadata at the top of the file, copy all the images to your blog's *images* directory and change the image links or other internal links to match the new path. 

This is not that difficult but it means you cannot test how your post will look on your blog until you are ready to publish it and you may have to update the image links in your post before you finish publishing it. 

There are other ways to work with a draft post that you can keep inside your blog project while still preventing it from getting published before you are ready.

### Images in draft posts

Create images in draft post's directory


Use the {attach} for images and store them in the same directory

```python
![test image in draft]({attach}image-draft.png)
```

Pelican will find the image when you test the draft and when you move both the post to your *content* directory and your images directory to *content/images*, Pelican will find the image when you rebuild the site.


## Use *status: draft* metadata

Optionally create a *content/drafts* directory and a *content/drafts/images* directory so you can keep your work in progress separated from your published content.

Keep in mind the the *output/drafts* file will have a naming convention defined by Pelican. 

By default, it creates a post file name based on the post's *slug* metadata. If you want to change that, use the settings and configure

https://docs.getpelican.com/en/latest/settings.html#url-settings

default values are:

```python
DRAFT_URL = 'drafts/{slug}.html'
DRAFT_SAVE_AS = 'drafts/{slug}.html'
DRAFT_PAGE_URL = 'drafts/pages/{slug}.html'
DRAFT_PAGE_SAVE_AS = 'drafts/pages/{slug}.html'
```

The item in the curly brackets is from the blog post's metadata, "slug". 


<!--
You can use the *slug* metadata like the default or you can create your own metadata. For example, you could add *file:* to all posts' metadata then change the settings to  

```python
DRAFT_URL = 'drafts/{file}.html'
DRAFT_SAVE_AS = 'drafts/{file}.html'
DRAFT_PAGE_URL = 'drafts/pages/{file}.html'
DRAFT_PAGE_SAVE_AS = 'drafts/pages/{file}.html'
```

We did not change the publishing variables so drafts will be saved according the the custom *file* metadata and published files will be saved according to the *slug* metadata.

You may define a custom path and filename for specific drafts by using the *save_as* metadata in the Markdown file. This way you don't have to set or remember how the Pelican settings cause Pelican to build the draft file name.
-->

Testing draft file

Draft files are not linked from the front page of the blog. To get to a draft post you must type in the full URL of the post

http://127.0.0.1:8000/drafts/this-is-a-test-post.html




## Use default metadata

One way to make draft posts appear on you local development version but not in production version is to use 

in *publishconf.py*

```python
DEFAULT_METADATA = {'status': 'draft',}
```

in *pelicanconf.py*

```python
DEFAULT_METADATA = {'status': 'published',}
```

Then do not define the *status* metadata in draft posts. They will be "published" on your local blog and "draft" on your published blog.

When you want to publish the draft, define the *status* metadata at the top of the post.

I like to comment-out the status metadata to remind myself I need to set it to published when I am ready

```
<!--status: published-->
```

Testing is easy. Just go to the local development blog at *http://127.0.0.1:8000/*. The draft post will be at the top, assuming it has the newest data in its metadata. But, if you re-deploy your site for any reason such as to update an older published post, the draft post will not appear on the published web site.

## Work in a new branch

If you publish your blog to a service prover using Git integration, then using a new Git branch may work for you.

If, while working on the draft, you need to update an existing blog post you must change back to the main branch.







### attaching images and organizing images in directories 

https://deaddabe.fr/blog/2020/08/30/using-and-extending-the-attach-directive-in-pelican/
https://docs.getpelican.com/en/3.6.3/content.html#attaching-static-files

https://dev.to/thebouv/building-my-static-site-with-pelican-part-one-330i
    --- uses Git submodules for output   https://git-scm.com/book/en/v2/Git-Tools-Submodules

    
