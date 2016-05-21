{% extends "base.tpl" %}
{% block body %}
    {% for post in posts %}
        <article class="post">
            <header class="post-header">
                <h2 class="post-title"><a href="{{ post.link }}">{{ post.title }}</a></h2>
            </header>
                <p>{{ post.summary }}</p>
        </article>
    {% endfor %}
    <p class="big-button"><a href="{{ SERVER_DOMAIN }}archive">{{ LANG_ARCHIVE }}</a></p>
{% endblock %}
