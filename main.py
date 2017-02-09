#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Typedown CMS
#
# Simple Python3 CMS built on top of Bottle
#
# A project that started out as a simple web application for local markdown
# files evolved into a blog engine and then naturally evolved into a content
# management system. It's built upon Bottle Web Framework and using techniques
# such as Markdown, RSS and Jinja2 templates.
#
# TODO: Add support for h1/h2 alternative header syntax === ---

__author__ = "Philip Andersen <philip.andersen@codeofmagi.net>"
__license__ = "MIT"
__version__ = "1.0"
__copyright__ = "Copyright 2016-2017 (c) Philip Andersen"


"""
Initialize application

- Import modules
- Read classes/functions
"""
try:

    # Python built-in
    import configparser
    import html.parser
    import collections
    import functools
    import datetime
    import fnmatch
    import os.path
    import glob
    import os

    # External
    import bottle as core
    import markdown
    import PyRSS2Gen
    import jinja2

except ImportError as e:

    # Kill process,print missing module name with instructions
    exit(
        str(e) +
        "\nTry install missing modules with 'pip3 install -r requirements.txt'"
    )


class Server:

    def check_flags():
        """ Checking for non-production flags is enabled """

        # Start out with no flags
        flags = 0

        # Check debug
        if cfg['server']['DEBUG'] == "True":
            Template.add_var('DEBUG', True)
            flags += 1

        # Check reloader
        if cfg['server']['RELOADER'] == "True":
            Template.add_var('RELOADER', True)
            flags += 1

        # Check if there was any flags and add to template
        if flags > 0:
            Template.add_var('ERROR_FLAGS', True)
            return True

    def read_config(filename, required=None):
        """ Get index and values from configuration files """

        try:
            # Try open the file
            with open(filename, 'r') as f:

                # Read configuration
                config = configparser.RawConfigParser()
                config.read_file(f)

                # Return index and values
                return config

        except IOError:

            # Print error message
            print(filename + ' cannot be found.')

            # Kill the process if it's a required configuration
            if required:
                exit()


class Template:

    def add_var(name, value):
        """ Add variable to template """
        core.Jinja2Template.defaults[name] = value

    def get_vars(category):
        """ Get variables from a configuration file category """
        for key, value in cfg[category].items():
            core.Jinja2Template.defaults[
                (category + '_' + key).upper()
            ] = value


class Text:

    def truncate(text, count, end='...'):
        """ Truncate text if less then 'count' """
        return text[:count] + end if len(text) > count else text

    def get_summary(mdfile, count=300):
        """ Get first paragraph from a Markdown document into plain text """

        # Set HTMLParser configuration
        class Html2Text(html.parser.HTMLParser):

            def __init__(self):
                super().__init__()
                self.reset()
                self.convert_charrefs = True
                self.container = ''

            def handle_data(self, data):
                self.container += data

            def return_data(self):
                self.close()
                return self.container

        # Open markdown file
        with open(mdfile, 'r', encoding='utf-8') as mdcontent:

            # Skip h1 and h2
            next(mdcontent)
            next(mdcontent)
            next(mdcontent)

            # Strip HTML
            strip = Html2Text()
            strip.feed(markdown.markdown(mdcontent.read()))

            # Truncate
            return Text.truncate(strip.return_data(), count)


class Post:

    def get_permalink(filepath, name):
        """ Return the full link of a post """

        # Remove relative path
        filepath = filepath.replace(cfg['path']['POSTS'], "archive/")

        # Split the date separator
        filepath = filepath.split('_', 1)[0]

        # Sort splitted data
        archive = filepath.split('/')[0]
        category = filepath.split('/')[1]
        date = filepath.split('/')[2].replace('-', '/')
        title = name.replace('.md', '')

        path = archive + '/' + category + '/' + date + '/' + title
        link = cfg['server']['DOMAIN'] + path

        # Return permalink url
        return link

    def get_posts(category=None, limit=None, title=None):
        """ Return posts, limit results with args """

        # Define variables
        (categories, posts, file_count, archive, stop) = [], [], 0, None, None

        # Set default file path
        filepath = cfg['path']['POSTS']

        # Check if to only show most recent posts, else show all
        if limit:
            limit = int(limit)

        # Check if it's a catagory request
        if category:
            filepath = cfg['path']['POSTS'] + category
            if not os.path.isdir(filepath):
                raise core.HTTPError(404)

        # Crawl for posts
        for root, dirnames, filenames in os.walk(filepath):
            for filename in fnmatch.filter(filenames, '*.md'):

                # Define filename
                filepath = root + '/' + filename
                filename_short = filename.split("_")[1].replace('.md', '')
                filename_link = cfg['server']['DOMAIN']+'post/'+filename_short

                # Define dateformat
                dateformat = datetime.datetime.strptime(
                    filename.split("_")[0], '%Y-%m-%d'
                )

                # Add post
                posts.append({
                    'filepath':
                        filepath,
                    'category':
                        filepath.split('/')[3],
                    'category_name':
                        filepath.split('/')[3].replace('-', ' '),
                    'title':
                        filename_short.replace('-', ' '),
                    'timestamp':
                        dateformat.strftime('%s'),
                    'date_YMD':
                        dateformat.strftime('%Y-%m-%d'),
                    'date':
                        dateformat.strftime(cfg['global']['TIME']),
                    'link':
                        filename_link,
                    'summary':
                        Text.get_summary(
                            filepath, int(cfg['global']['TRUNCATE_C'])
                        )
                })

                # Loop counter
                file_count += 1

                # Limit break
                if limit and file_count == limit:
                    stop = True
                    break

            # Break outer loop
            if stop:
                break

        # Sort the posts by time, newest first
        posts.sort(key=lambda item: item['timestamp'], reverse=True)

        # Switch title
        if title is None:
            if limit:
                title = cfg['lang']['RECENT_POSTS']
            else:
                title = cfg['lang']['ARCHIVE']

        # Return posts
        return {
            'title':
                title,
            'posts':
                posts,
            'category':
                category,
            'category_name':
                category.replace('-', ' ') if category else None,
            'categories':
                Dir.get_categories(links=True),
            'url':
                core.request.url,
            'type':
                'archive' if category else 'category',
            'post_count':
                file_count
        }


class Dir:

    def get_subfolders(dir):
        """ Return a list of subfolders """
        return [name for name in os.listdir(dir)
                if os.path.isdir(os.path.join(dir, name))]

    def get_categories(dir='content/posts', links=True):
        """ Return a list of categories, with link """

        # Define container
        categories = []

        # Crawl folders
        for folder in Dir.get_subfolders(dir):
            if links:
                categories.append({
                    'title': folder.replace('-', ' '),
                    'link': cfg['server']['DOMAIN']+'archive/'+folder
                })
            else:
                categories.append({'title': folder})

        # Return list of categories
        return categories


class Page:

    def get_hero(name):
        """ Return hero image file by post/page name """

        # Check each extension
        for item in ['jpg', 'jpeg', 'png']:

            # Relative path name to image
            filepath_ext = cfg['path']['HERO'] + name + '.' + item

            # Check if image exists and return it
            if os.path.isfile(filepath_ext):
                return cfg['server']['DOMAIN'] + filepath_ext

    def get_content(filename, convert_markdown=True, template=True):
        """ Return page content """

        try:
            with open(filename, 'r', encoding='utf-8') as page:

                # Grab title and skip it from content
                title = page.readline()[1:]
                next(page)

                # Convert markdown
                if convert_markdown:
                    content = markdown.markdown(
                        page.read(), ['markdown.extensions.extra']
                    )
                else:
                    content = page.read()

                # Templating
                if template:
                    return {'title': title, 'content': content}
                else:
                    return content

        except IOError:
            raise core.HTTPError(404)


class Site:

    def get_menu(links={}):
        """ Return a dict with links """

        # Crawl pages
        for page in sorted(glob.glob(cfg['path']['PAGES'] + '*.md')):

            url = os.path.splitext(os.path.basename(page))[0]
            name = url.replace('-', ' ')

            # Check if to skip the Home-link
            if name == 'home' and cfg['global']['HOME_LINK'] == 'None':
                pass
            else:
                links[name] = cfg['server']['DOMAIN'] + url

        # Add blog-link if enabled
        if cfg['global']['blog'] == 'True':
            links[cfg['lang']['posts']] = cfg['server']['DOMAIN'] + 'posts'

        # Return a list with links
        return collections.OrderedDict(sorted(links.items()))

    def get_feed(summary=None):
        """ Return a RSS-feed """

        # Check if RSS is enabled
        if not cfg['global']['rss'] == "True":
            raise core.HTTPError(404)

        # Create containers
        (post, posts, items) = [], {}, []

        # Crawl posts
        for root, dirnames, filenames in os.walk(cfg['path']['POSTS']):
            for filename in fnmatch.filter(filenames, '*.md'):

                # Set filepath
                filepath = root + '/' + filename

                # Grab title
                title = filename.split("_")[1].replace('.md', '')

                # Define date
                date = datetime.datetime.strptime(
                    filename.split("_")[0], '%Y-%m-%d'
                )

                # Truncate content if summary RSS
                if summary:
                    description = Text.get_summary(
                        filepath,
                        int(cfg['global']['TRUNCATE_C'])
                    )
                    file_output = 'static/feed.xml'
                else:
                    description = Page.get_content(filepath, template=False)
                    file_output = 'static/feed-full.xml'

                # Add post
                post.append({
                    'title':
                        title.replace("-", " "),
                    'link':
                        cfg['server']['DOMAIN'] + 'post/' + title,
                    'description':
                        description,
                    'guid':
                        Post.get_permalink(filepath, title),
                    'pubDate':
                        date.strftime("%a, %d %b %Y %z"),
                    'timestamp':
                        date.strftime('%s')
                })

        # Sort posts by date, newest first
        post.sort(key=lambda item: item['timestamp'], reverse=True)

        # RSS items
        for item in post:
            items.append(PyRSS2Gen.RSSItem(
                title=item['title'],
                link=item['link'],
                description=item['description'],
                guid=item['guid'],
                pubDate=item['pubDate']
            ))

        # RSS overall content
        rss = PyRSS2Gen.RSS2(
            title=cfg['global']['SITENAME'],
            link=cfg['server']['DOMAIN'],
            description=cfg['global']['DESCRIPTION'],
            lastBuildDate=datetime.datetime.now(),
            items=items
        )

        # Write contents to xml-file
        try:
            with open(file_output, "w") as feed:
                rss.write_xml(feed, cfg['global']['CHARSET'])
        except IOError:
            raise core.HTTPError(404)

        # Return the xml file
        return core.static_file(file_output, root=cfg['path']['ROOT'])


if __name__ == '__main__':
    """ Main application

    - Initialize core
    - Read system configuration
    - Setup view
    - Add global variables
    - Check server flags
    - Application routing
    """

    # Initialize Bottle
    app = core.Bottle()

    # Read configuartion
    cfg = Server.read_config('settings.cfg', required=True)

    # Setup view and Jinja2
    views = (
        cfg['path']['ROOT'] + 'static/themes/' +
        cfg['global']['THEME'] + '/views'
    )
    view = functools.partial(core.jinja2_view, template_lookup=[views])

    # Get vars for templates
    Template.get_vars('global')
    Template.get_vars('lang')

    # Add some extra vars
    Template.add_var('year', datetime.datetime.now().year)
    Template.add_var('menu', Site.get_menu())
    Template.add_var('SERVER_DOMAIN', cfg['server']['DOMAIN'])

    Template.add_var('GENERATOR', 'Typedown CMS 1.0')
    Template.add_var(
        'GLOBAL_THEME_PATH',
        cfg['server']['DOMAIN'] + 'static/themes/' + cfg['global']['THEME']
    )

    # Check the state of server
    Server.check_flags()

    """
    Application routing

    - Error handling
    - RSS Feed
    - Static files
        - Favicon
        - Robots
        - Hero
    - Index /
        - /home
        - /page
        - /posts
        - /archive
        - /archive/category
        - /post/shortname
        - /archive/date/shortname (Post permalink)
    """
    @app.error(404)
    @app.error(500)
    @view('base.tpl')
    def error(code):
        return {'error': code}

    @app.route('/feed/summary')
    @app.route('/feed/summary/')
    def summary_feed():
        return Site.get_feed(summary=True)

    @app.route('/feed')
    @app.route('/feed/')
    def full_feed():
        return Site.get_feed()

    @app.route('/static/<filepath:path>')
    def get_static(filepath):
        response = core.static_file(
            filepath,
            root='{}static'.format(cfg['path']['ROOT'])
        )
        response.set_header("Cache-Control", "public, max-age=604800")
        return response

    @app.route('/favicon.ico')
    def get_favicon():
        return get_static('favicon/favicon.ico')

    @app.route('/robots.txt')
    def get_robots():
        response = core.static_file(
            'static/robots.txt', root=format(cfg['path']['ROOT'])
        )
        response.set_header("Cache-Control", "public, max-age=604800")
        return response

    @app.route('/' + cfg['path']['HERO'] + '<filepath:path>')
    def get_content_hero(filepath):
        return core.static_file(
            filepath, root='{}'.format(cfg['path']['ROOT']+cfg['path']['HERO'])
        )

    @app.route('/')
    def index():
        return core.redirect('/' + cfg['global']['INDEX_NAME'])

    @app.route('/' + cfg['global']['INDEX_NAME'])
    @app.route('/' + cfg['global']['INDEX_NAME'] + '/')
    @view('home.tpl')
    def home(blog=None):

        # Reload configuration, template variables  and menu
        global cfg
        cfg = Server.read_config('settings.cfg', required=True)
        Template.get_vars('global')
        Template.get_vars('lang')
        Template.add_var('menu', Site.get_menu())

        # Show recent posts ?
        if cfg['global']['INDEX_POSTS'] == "True":
            blog = Post.get_posts(limit=cfg['global']['RECENT_POSTS'])

        # Load home page
        try:
            page = Page.get_content(cfg['path']['PAGES'] + "home.md")
            return {
                'title':
                    page['title'],
                'content':
                    page['content'],
                'blog':
                    blog,
                'hero':
                    Page.get_hero('home'),
                'url':
                    core.request.url,
                'type':
                    'home'
            }
        except IOError:
            raise core.HTTPError(404)

    @app.route('/<name>', method='GET')
    @view('page.tpl')
    def get_page(name):

        # Load page content
        try:
            page_contents = Page.get_content(
                cfg['path']['PAGES'] + name + ".md"
            )
            return {
                'content':
                    page_contents['content'],
                'title':
                    page_contents['title'],
                'hero':
                    Page.get_hero(name),
                'url':
                    core.request.url,
                'type':
                    'page',
                'page':
                    True
            }
        except IOError:
            raise core.HTTPError(404)

    @app.route('/posts')
    @app.route('/posts/')
    @view('posts.tpl')
    def get_post():
        return Post.get_posts(limit=cfg['global']['RECENT_POSTS'])

    @app.route('/archive')
    @app.route('/archive/')
    @view('archive.tpl')
    def get_archive():
        return Post.get_posts()

    @app.route('/archive/<name>')
    @app.route('/archive/<name>/')
    @view('archive.tpl')
    def get_category(name):
        return Post.get_posts(category=name)

    @app.route('/post/<name>')
    @app.route('/post/<name>/')
    @view('post.tpl')
    def get_post_shortname(name):

        # Define filename
        filename = glob.glob(cfg['path']['POSTS'] + '/*/*_' + name + '.md')

        # Get permalink and and check if post exists
        try:
            permalink = Post.get_permalink(filename[0], name)
        except IndexError:
            raise core.HTTPError(404)

        # Get post content
        for name in filename:
            post = Page.get_content(name, True)
            post_raw = Page.get_content(name, False)
            date_YMD = name.split("/")[4].split("_")[0]
            date = datetime.datetime.strptime(date_YMD, '%Y-%m-%d')

        # Return post
        return {
            'content':
                post['content'],
            'permalink':
                permalink,
            'date':
                date.strftime(cfg['global']['TIME']),
            'date_YMD':
                date_YMD,
            'category':
                name.split('/')[3],
            'category_link':
                name.split('/')[3].replace('/', '-'),
            'category_name':
                name.split('/')[3].replace('-', ' '),
            'title':
                post['title'],
            'intro':
                post_raw['content'].split('\n')[1][2:],
            'hero':
                Page.get_hero(name.split('_')[1].replace('.md', '')),
            'url':
                core.request.url,
            'type':
                'post'
        }

    @app.route('/archive/<category>/<year:int>/<month:int>/<day:int>/<name>')
    @app.route('/archive/<category>/<year:int>/<month:int>/<day:int>/<name>/')
    @view('post.tpl')
    def get_post_date(category, year, month, day, name):

        # Sort out the filename
        filepath = cfg['path']['ROOT'] + "content/posts/" + category + "/"

        # Sort out the date
        filedate = "{}-{}-{}_{}".format(
            str(year).zfill(2),
            str(month).zfill(2),
            str(day).zfill(2),
            name
        )

        # Set filename
        filename = filepath + filedate + ".md"

        # Get post contents
        post = Page.get_content(filename, True)
        post_raw = Page.get_content(filename, False)
        date_YMD = filename.split("/")[4].split("_")[0]
        date = datetime.datetime.strptime(date_YMD, '%Y-%m-%d')

        # Return the post
        return {
            'content':
                post['content'],
            'permalink':
                Post.get_permalink(filename, name),
            'date':
                date.strftime(cfg['global']['TIME']),
            'date_YMD':
                date_YMD,
            'title':
                post['title'],
            'hero':
                Page.get_hero(name),
            'category':
                category,
            'category_link':
                category,
            'category_name':
                category.replace('-', ' '),
            'intro':
                post_raw['content'].split('\n')[1][2:],
            'url':
                core.request.url,
            'type':
                'post'
        }

    # Run it
    core.run(
        app=app,
        host=cfg['server']['HOST'],
        port=cfg['server']['PORT'],
        reloader=cfg['server']['RELOADER'],
        debug=cfg['server']['DEBUG']
    )
