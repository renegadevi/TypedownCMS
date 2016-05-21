{% extends "base.tpl" %}
{% block body %}
    {{ content }}
    {% if blog %}
    <div id="home-blog">
        <!-- <h2>{{ LANG_RECENT_POSTS }}</h2> -->
        {% for post in blog.posts %}
        <article class="post">
            <header class="post-header">
                <h3 class="post-title"><a href="{{ post.link }}">{{ post.title }}</a></h3>
                <p>
                    <a href="{{ SERVER_DOMAIN }}archive/{{ post.category }}">{{ post.category_name | capitalize }}</a>
                    {{ LANG_AT }} <time class="post-date" datetime="{{ post.date_YMD }}">{{ post.date }}</time>
                </p>
            </header>
            <div class="post-summary">
                <p>{{ post.summary }} <a class="read-more" href="{{ post.link }}">{{ LANG_READ_MORE }}</a></p>
            </div>
        </article>
        {% endfor %}
    </div>
    {% endif %}
{% endblock %}
