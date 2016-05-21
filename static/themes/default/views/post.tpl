{% extends "base.tpl" %}
{% block body %}
<article class="post">
    <section class="post-content">
        {{ content }}
    </section>
    {% if GLOBAL_DISQUS %}
    <footer class="post-footer">
        <!-- /START DISQUS GENERATED CODE -->
        <div id="disqus_thread"></div>
        <script type="text/javascript">
            var disqus_shortname = '{{ GLOBAL_DISQUS }}';
            (function() {
                var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
                dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
                (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
            })();
        </script>
        <!-- /END DISQUS GENERATED CODE -->
    </footer>
    {% endif %}
</article>
{% endblock %}
