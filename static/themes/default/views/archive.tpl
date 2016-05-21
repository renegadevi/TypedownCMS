{% extends "base.tpl" %}
{% block body %}
    {% for post in posts %}
        <article class="post">
            <header class="post-header">
                <h2 class="post-title"><a href="{{ post.link }}">{{ post.title }}</a></h2>
                    <p class="post-meta">
                        <a href="{{ SERVER_DOMAIN }}archive/{{ post.category }}">{{ post.category_name | capitalize }}</a>
                        {{ LANG_AT }} <time class="post-date" datetime="{{ post.date_YMD }}">{{ post.date }}</time>
                    </p>
            </header>
             <p class="read-more">{{ post.summary }}<a href="{{ post.link }}">{{ LANG_READ_MORE }}</a></p>
        </article>
    {% endfor %}
{% endblock %}
