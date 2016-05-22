<!DOCTYPE html>
<html lang="{{ GLOBAL_LANG }}">
    <head>
        {% block head %}
        <meta charset="{{ GLOBAL_CHARSET }}">
        <title>
            {{ GLOBAL_SITENAME }}
            {% if type == "category" %}
                {% if not category == None %}
                    - {{ category|title }}
                {% endif %}
            {% endif %}

            {% if title %}
                {% if type == "home" %}
                    - {{ GLOBAL_DESCRIPTION }}
                {% else %}
                    {% if category and type == "post" %}
                        - {{ category|title }}
                        - {{ title|title|striptags }}
                    {% elif category %}
                        - {{ title|title|striptags }}
                        - {{ category|title }}
                    {% else %}
                        - {{ title|title|striptags }}
                    {% endif %}
                {% endif %}
            {% endif %}

            {% if error %}
                - {{ error.status_line }}
            {% endif %}
        </title>

        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="generator" content="{{ GENERATOR }}" />

        <meta name="description" content="{{ GLOBAL_DESCRIPTION }}">
        <link rel="author license copyright" title="{{ GLOBAL_SITENAME }}" href="{{ SERVER_DOMAIN }}">

        {% if GLOBAL_RSS == "True" %}
        <!-- RSS Feeds -->
        <link rel="alternate" type="application/rss+xml" title="{{ GLOBAL_SITENAME }} - RSS Full text" href="{{ SERVER_DOMAIN }}feed" />
        <link rel="alternate" type="application/rss+xml" title="{{ GLOBAL_SITENAME }} - RSS Summary" href="{{ SERVER_DOMAIN }}feed/summary" />
        {% endif %}

        <!-- Stylesheets -->
        <link rel="stylesheet" media="all" type="text/css" href="{{ GLOBAL_THEME_PATH }}/css/normalize-4.1.1.css"/>
        <link rel="stylesheet" media="screen" type="text/css" href="{{ GLOBAL_THEME_PATH }}/css/screen.css"/>
        <link rel="stylesheet" media="print" type="text/css" href="{{ GLOBAL_THEME_PATH }}/css/print.css"/>
        <link rel="stylesheet" media="print" type="text/css" href="{{ GLOBAL_THEME_PATH }}/css/github-markdown.css"/>

        <!-- Favicon

        A Bunch of Favicon variants, because everyone can't just support a
        unified method with png/svg, some of these lines isn't even valid html5
        -->
        <link rel="icon" type="image/x-icon" href="{{ SERVER_DOMAIN }}favicon.ico" />

        <link rel="apple-touch-icon" sizes="57x57"   href="{{ SERVER_DOMAIN }}static/favicon/apple-touch-icon-57x57.png">
        <link rel="apple-touch-icon" sizes="60x60"   href="{{ SERVER_DOMAIN }}static/favicon/apple-touch-icon-60x60.png">
        <link rel="apple-touch-icon" sizes="72x72"   href="{{ SERVER_DOMAIN }}static/favicon/apple-touch-icon-72x72.png">
        <link rel="apple-touch-icon" sizes="76x76"   href="{{ SERVER_DOMAIN }}static/favicon/apple-touch-icon-76x76.png">
        <link rel="apple-touch-icon" sizes="114x114" href="{{ SERVER_DOMAIN }}static/favicon/apple-touch-icon-114x114.png">
        <link rel="apple-touch-icon" sizes="120x120" href="{{ SERVER_DOMAIN }}static/favicon/apple-touch-icon-120x120.png">
        <link rel="apple-touch-icon" sizes="144x144" href="{{ SERVER_DOMAIN }}static/favicon/apple-touch-icon-144x144.png">
        <link rel="apple-touch-icon" sizes="152x152" href="{{ SERVER_DOMAIN }}static/favicon/apple-touch-icon-152x152.png">
        <link rel="apple-touch-icon" sizes="180x180" href="{{ SERVER_DOMAIN }}static/favicon/apple-touch-icon-180x180.png">

        <link rel="icon" type="image/png" sizes="16x16"   href="{{ SERVER_DOMAIN }}static/favicon/favicon-16x16.png">
        <link rel="icon" type="image/png" sizes="32x32"   href="{{ SERVER_DOMAIN }}static/favicon/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="96x96"   href="{{ SERVER_DOMAIN }}static/favicon/favicon-96x96.png">
        <link rel="icon" type="image/png" sizes="192x192" href="{{ SERVER_DOMAIN }}static/favicon/android-chrome-192x192.png">

        <link rel="manifest" href="{{ SERVER_DOMAIN }}static/favicon/manifest.json">
        <link rel="mask-icon" href="{{ SERVER_DOMAIN }}static/favicon/safari-pinned-tab.svg" color="#d47a7a">
        <meta name="apple-mobile-web-app-title" content="{{ GLOBAL_SITENAME }}">
        <meta name="application-name" content="{{ GLOBAL_SITENAME }}">
        <meta name="theme-color" content="#ffffff">

        {% if hero %}
        <style>
        .hero {
          background:
          linear-gradient(
            to bottom,
            rgba(44, 42, 36, .8) 0%,
            rgba(20, 20, 20, .4) 100%
          ), url('{{ hero }}') no-repeat center center;
            background-size: cover;
        }
        </style>
        {% else %}
        <style>
        .hero {
            background:
            linear-gradient(
              to bottom,
              rgba(44, 42, 36, .8) 0%,
              rgba(20, 20, 20, .4) 100%
            ), url('{{ SERVER_DOMAIN }}content/hero/default.jpg') no-repeat center center;
            background-size: cover;
        }
        </style>
        {% endif %}
        {% endblock %}
	</head>

    <body class="fade-in one">
        {% if ERROR_FLAGS %}
            <div class="warning">
                <p><strong>Warning</strong>: Development mode, there's still non-productive flags active.</p>
            </div>
        {% endif %}

        <header class="hero">
            <div id="top">
                <div class="wrapper-fluid">
                    <!-- Main logo -->
                    <div id="top-logo">
                        <a href="{{ SERVER_DOMAIN }}" title="{{ GLOBAL_SITENAME }}">
                          {% if GLOBAL_SHOW_LOGO == "True" %}
                          <img src="{{ GLOBAL_THEME_PATH }}/img/logo.svg" title="{{ GLOBAL_SITENAME }}" alt="">
                          {% else %}
                          {{ GLOBAL_SITENAME }}
                          {% endif %}
                        </a>
                    </div>
                    <!-- Main navigation -->
                    <label id="label-mobile" for="nav"><img src="{{ GLOBAL_THEME_PATH }}/img/icons/arrows_hamburger2_white.svg" class="icon-menu-folded" alt=""></label>
                    <nav id="top-nav">
                        <input type="checkbox" id="nav" />
                        <ul>
                            {% if GLOBAL_RSS == "True" %}
                            {% if GLOBAL_RSS_LINK == "True" %}
                            <li id="sublist-rss" class="submenu">
                                <label id="label-rss" for='item-1'>Subscribe
                                </label>
                                <input type="checkbox" id="item-1"/>
                                <ul>
                                    <li><a href="{{ SERVER_DOMAIN }}feed" target="_blank">Full</a></li>
                                    <li><a href="{{ SERVER_DOMAIN }}feed/summary" target="_blank">Summary</a></li>
                                </ul>
                            </li>
                            {% endif %}
                            {% endif %}

                            {% for title, link in menu.items() %}
                                <li><a href="{{link}}">{{ title|capitalize }}</a></li>
                            {% endfor %}
                        </ul>
                    </nav>
                </div>
            </div>
            <div class="table-auto">
                {% if type == "home" %}
                <div id="top-content-home" class="wrapper">
                {% else %}
                <div id="top-content" class="wrapper">
                {% endif %}
                    {% if title %}

                        {% if type == "archive" %}
                        <h1>{{ title }} <span class="desc">"{{ category_name|title }}"</span></h1>
                        {% else %}
                            {% if type == "post" %}
                            <h1>
                                <a href="{{ permalink }}">{{ title }}</a>
                                <span class="small screen-only">
                                    <a href="{{ permalink }}" title="{{ LANG_PERMALINK }}">
                                        <img alt="" src="{{ GLOBAL_THEME_PATH }}/img/icons/basic_link_white.svg" class="icon-small">
                                    </a>
                                </span>
                            </h1>
                            {% else %}
                            <h1>{{ title }}</h1>
                            {% endif %}
                        {% endif %}

                    {% endif %}
                    {% if error %}
                    <h1>{{ error.status_line }}</h1>
                    {% endif %}
                    {% if type == "post" %}
                    <section class="post-meta">
                        <p>
                            <a href="{{ SERVER_DOMAIN }}archive/{{ category_link }}">{{ category_name | capitalize }}</a>
                            {{ LANG_ON }} <time class="post-date" datetime="{{ date_YMD }}">{{ date }}</time>
                        </p>
                    </section>
                    {% elif url == SERVER_DOMAIN+"archive" %}
                    <section class="post-meta meta-categories">
                        <p>{{ LANG_CATEGORIES }}:</p>
                        <ul class="clean-list">
                            {% for category in categories %}
                            <li><a href="{{ category.link }}" title="{{ category.title | capitalize }}">{{ category.title | capitalize }}</a></li>
                            {% endfor %}
                        </ul>
                    </section>
                    {% endif %}
                </div>
            </div>
        </header>
        {% if type == "home" %}
        <main id="content-home" class="wrapper-fluid padding fade-in two">
        {% else %}
        <main id="content" class="wrapper-fluid padding fade-in two">
        {% endif %}

            {% block body %}
            {% endblock %}
        </main>

        {% block footer %}
        <footer id="bottom" class="wrapper-fluid">
            <p class="float-left">Copyright {{ year }} <strong>
              {{ GLOBAL_SITENAME }}</strong></p>
            <p class="float-right">Published with <strong>TypedownCMS</strong></p>
        </footer>
        <div class="print-only">
            <hr>
            <p>Source: <br> {{ url }}</p>
        </div>
        {% endblock %}
        {% if GLOBAL_ANALYTICS %}
        <script>
        (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
            (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
            m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
        })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

        ga('create', '{{ GLOBAL_ANALYTICS }}', 'auto');
        ga('send', 'pageview');
        </script>
        {% endif %}
	</body>
</html>
