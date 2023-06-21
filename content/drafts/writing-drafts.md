title: Writing drafts for Pelican blogs
slug: writing-drafts
summary: Here are some tips for conveniently working on draft blog posts for your Pelican blog while keeping your work in progress from appearing on your published web site.
date: 2023-05-15
modified: 2023-05-15
category: Blogging
<!--status: draft-->

When you work on a post for your Pelican-based blog, you probably don't want the draft post to appear on your published blog. But, that could happen if, while you are working on a draft for your next post, you re-deploy your blog. Here are some tips for conveniently working on draft blog posts for your Pelican blog while keeping your work in progress from appearing on your published web site.

## Work in a different folder

The simplest method is to set up a folder that contains the Markdown file for your future post plus any other files you need like images. Edit the Markdown file and test the way the post will look using a Markdown preview feature in your text editor or a separate preview application.

Then, when it is time to publish the post, add the metadata at the top of the file, copy all the images to your blog's *images* directory and change the image links or other internal links to match the new path. 

This is not that difficult but it means you cannot test how your post will look on your blog until you are ready to publish it. There are other ways to work with a draft post that you can keep inside your blog project while still preventing it from getting published before you are ready.

## Use *status: draft* metadata

Keep in mind the the *output/drafts* file will have a naming convention defined by Pelican. 

By default, it creates a post file name based on the post's *slug* metadata. If you want to change that, use the settings and configure

https://docs.getpelican.com/en/latest/settings.html#url-settings

DRAFT_URL = 'drafts/{slug}.html'
DRAFT_SAVE_AS = 'drafts/{slug}.html'
DRAFT_PAGE_URL = 'drafts/pages/{slug}.html'
DRAFT_PAGE_SAVE_AS = 'drafts/pages/{slug}.html'

The item in the curly brackets is from the blog post's metadata. You can use the *slug* metadata like the default or you can create your own metadata. For example, you could add *file:* to all posts' metadata then change the settings to  

DRAFT_URL = 'drafts/{file}.html'
DRAFT_SAVE_AS = 'drafts/{file}.html'
DRAFT_PAGE_URL = 'drafts/pages/{file}.html'
DRAFT_PAGE_SAVE_AS = 'drafts/pages/{file}.html'

We did not change the publishing variables so drafts will be saved according the the custom *file* metadata and published files will be saved according to the *slug* metadata.

You may define a custom path and filename for specific drafts by using the *save_as* metadata in the Markdown file. This way you don't have to set or remember how the Pelican settings cause Pelican to build the draft file name.

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

## Images in draft posts

When testing the draft post, image links and other internal links will break because they are not changed when the post is published to the drafts folder. 

Probably best to work with a Markdown editor and preview the page in the editor if you need to check images and links.

> OR use the {static} placeholder in the post??? MAybe this helps keep the links working?

