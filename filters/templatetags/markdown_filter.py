# https://jamie.curle.io/blog/minimal-markdown-template-tag-django/
from django import template
register = template.Library()

import markdown

class MarkDownNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        return markdown.markdown(self.nodelist.render(context))

@register.tag('markdown')
def markdown_tag(parser, token):
    """
    Enables a block of markdown text to be used in a template.

    Syntax::

            {% markdown %}
            ## Markdown
            
            Now you can write markdown in your templates. This is good because:
            
            * markdown is awesome
            * markdown is less verbose than writing html by hand
            
            {% endmarkdown %}
    """
    nodelist = parser.parse(('endmarkdown',))
    # need to do this otherwise we get big fail
    parser.delete_first_token()
    return MarkDownNode(nodelist)