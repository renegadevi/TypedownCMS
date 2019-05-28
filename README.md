# Typedown CMS
Flat-File Markdown CMS built with Python 3

![Screenshot](http://i.imgur.com/54kntZi.png)

## Features
* Markdown
* Flat-file + Cloud-sync
* Disqus
* Statistics
* RSS
* Jinja2
* Mobile-First
* Printer-friendly
* FOSS

## Hello there, Welcome
I started out this project as a simple markdown document reader for my self as there was a lot of alternatives out there but I wanted something that would make publishing simple. This is my first project with  Bottle as a Micro Framework for Python 3 and I liked it, during it's development it evolved into a CMS with a lot more features but still keep things simple, flexible and flat-file.

## Installation
the only requirement is Python3 which is the now and the future of Python language. It has been tested on following systems. See install-guides for Ubuntu, CentOS and OSX El Capitan down below including how to install python3.

| OS				| Python version	|
| :-----------------|------------------:|
| MacOS Mojave      | 3.7.3             |

### Quickstart (TL;DR)
1. Clone repo
2. Create virtualenv
3. Install pip-requirements (modules)
4. Run main.py
5. Locate to [http://localhost:8080/](http://localhost:8080/ "http://localhost:8080/")


### Installation guide: MacOS Mojave

```sh
# Install Brew package manager
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

# Install Python 3 and git
brew install python3 git

# Clone git repo
git clone https://gitlab.com/renegadevi/TypedownCMS.git

# Enter folder
cd TypedownCMS

# Create a virtual (isolated) enviroment
virtualenv -p /usr/local/bin/python3 venv

# Enable enviroment
source venv/bin/activate

# Install required modules
pip3 install -r requirements.txt

# Make app executable
chmod +x main.py

# Run server
./main.py
```

## Getting Started (post-installation)

### Configuration and setup
Now when you have TypedownCMS up and running, you can start using the CMS and make changes. There's a global configuration file named "***settings.cfg"*** where you can set settings very easy. For a specific walktrough for each setting, check our post over at ***(TODO)***. After you have saved the settings, the changes updates next time you visit the home/main page of your website.

#### Server settings (optional)

Default settings is setup as a development-enviroment where your local machine has access to it from your browser via the localhost address. When you move to Testing, by setting the domain to 0.0.0.0 your computer will be reacable by your IP-adress on your local network by other devices, example: http://192.168.1.102:8080/.

When your site is done and ready for production, change the domain to whatever domain you want it to be (or IP) and by changing the port from 8080 to 80 you do not need to type the port, however you need admin (root) privileges to use it.  So you would have to run `sudo ./main.py` insted of just `./main.py`

**Development**
- domain = http://localhost:8080/
- port = 8080

**Testing**
- domain = http://0.0.0.0:8080/
- port = 8080

Production
- domain =  http://yourdomain.com/
- port = 80


#### Running the server application (optional)
For development/testing purposes you can simply start it by using the command `./main.py` as a normal-user pointed out in the installation guide.

##### Production use
For production use you may in the end want to use something such as **uWSGI, Gunicorn** or **Nginx etc.** because it's a lot more reliable solution. However when you want something with a easy setup and portable I have written a "***autoloop.sh"***-script which is a wrapper for ***"main.py"***. What it does is if the python-script would fail, crash or something happends it autostarts as if nothing happen.

```sh
# Make autoloop.sh executable
chmod +x autoloop.sh

# If in production use with port 80, run as root/administrator
sudo ./autoloop.sh
```

### Create documents (Markdown > HTML)
TypedownCMS are using Markdown-syntax for both Pages and Blog posts. Markdown is a minimal syntax formatting for your douments that is clean and strucutred and portable; also backwards-compatable with HTML. All documents for  should start with a Title and Subtitle (h1/h2) as this example below. When visiting the home/main page it reloads the indexing of pages/blog-posts.

> \# This is the title of the page
>
> \## This is the subtitle
>
> This is some text on the page or a new blog post

*For more information regarding Markdown, check out this link:* [https://guides.github.com/features/mastering-markdown/**](https://guides.github.com/features/mastering-markdown/ "https://guides.github.com/features/mastering-markdown/")

#### Create a page
A**ll pages are saved at:** */content/pages/*

Save the document with the title you want on the page. When you save a markdown document as ***"about-me.md"***. The menu-title will be ***"About Me"*** and the url (slug) would be ***domain.com/about-me***

#### Create a blog post
A**ll blog posts are saved at:** */content/posts/< category-name >/*

When saving a document as a blog post you have to specify the category, date and title. Categories are simple sub-folders within the posts folder.  To identify date and title it's important to format the filename as ***"YYYY-MM-DD_Title.md"***; e.g ***"2016-01-02_My-New-Blog.md"***.

### Featured image "hero/header-image"
A**ll images are located at:** */content/hero/*

You can very simply use a image for each page/blog-post. It's all defined within the theme used. Name the image the same as the name such as ***"My-New-Blog.jpg"*** or ***"About-Me.jpg"***. Supported file formats is 'jpg, jpeg, png' and as a fallback on all pages there us a ***default.jpg***.

## License(s)

TypedownCMS is free and open-source software. It's released under the MIT license.  A permissive license that lets anyone to modify the code and use it however they want without any restrictions how to distribute it.

External resources:
- [Normalize.css](https://github.com/necolas/normalize.css/), MIT-license
- [Pixabay](https://github.com/Pixabay), Creative Commons CC0
- [Linea Iconset](http://linea.io "Linea Iconset"), CCBY License
- [github-markdown-css](https://github.com/sindresorhus/github-markdown-css "github-markdown-css"),  MIT-license
