from datetime import datetime

AUTHOR = 'Brian Linkletter'
SITENAME = 'Learning with Code'
SITEURL = 'https://learningwithcode.com'
LINKS = (('My other blog', 'https://brianlinkletter.com/'),)
SOCIAL = (("github", "https://github.com/blinklet"), ('linkedin', 'https://www.linkedin.com/in/brianlinkletter/'), ('twitter', 'http://twitter.com/belinkletter'),)
STATIC_PATHS = ['images']
PAGE_PATHS = ['pages']
ARTICLE_PATHS = ['']
SUMMARY_MAX_LENGTH = None
TIMEZONE = 'America/Toronto'
DEFAULT_LANG = 'en'
DEFAULT_PAGINATION = 10
RELATIVE_URLS = True
DEFAULT_CATEGORY = 'Python'
MARKDOWN = {'extension_configs': {'markdown.extensions.codehilite': {'css_class': 'highlight'}, 'markdown.extensions.extra': {}, 'markdown.extensions.meta': {}, 'markdown.extensions.admonition': {}, 'markdown.extensions.toc': {}}, 'output_format': 'html5'}
OUTPUT_PATH = 'output/'
PATH = 'content/'
THEME = 'Flex-2.5.0'
THEME_STATIC_DIR = 'theme'
FEED_ATOM = None
FEED_ATOM_URL = None
FEED_RSS = None
FEED_RSS_URL = None
FEED_DOMAIN = None
FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None


SITELOGO = ''
FAVICON = ''
SITESUBTITLE = 'Learning how to use Python for work and for fun'
SITEDESCRIPTION = 'Learning how to use Python for work and for fun: Data science, networking, internet of things'
USE_GOOGLE_FONTS = True
BROWSER_COLOR = '#333333'
PYGMENTS_STYLE = 'monokai'
MAIN_MENU = True
MENUITEMS = (("Categories", "/categories.html"),)
COPYRIGHT_YEAR = datetime.now().year
CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike 4.0 International License",
    "version": "4.0",
    "slug": "by-sa",
    "icon": True,
    "language": "en_US",
}
HOME_HIDE_TAGS = True
DISABLE_URL_HASH = True
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
THEME_COLOR_ENABLE_USER_OVERRIDE = True

