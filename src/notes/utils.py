import markdown
import bleach

from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
import xml.etree.ElementTree as etree
#from django.utils.safestring import mark_safe

ALLOWED_PROTOCOLS = {'http', 'https'}

ALLOWED_TAGS = [
    'p', 'hr', #'br'
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'blockquote',
    'ul', 'ol', 'li',
    'pre', 'code',
    'a',
    'em', 'strong',
    'img', 'iframe'
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt'],
    'iframe': ['src', 'title', 'allow', 'referrerpolicy', 'frameborder']
}

EMBED_RE = r'!\[([^\]]*)\]\(embed:([^)]+)\)'

class EmbedInlineProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        title = m.group(1)
        url = m.group(2)

        iframe = etree.Element("iframe")
        iframe.set("src", url)
        iframe.set("referrerpolicy", "strict-origin-when-cross-origin")
        iframe.set("frameborder", "0")
        # iframe.set("allowfullscreen", "true")

        if title:
            iframe.set("title", title)

        return iframe, m.start(0), m.end(0)

class Yt2iframe(Extension):
   def extendMarkdown(self, md):
       md.inlinePatterns.register(
                  EmbedInlineProcessor(EMBED_RE, md),
                  "embed",
                  175
        )

def markdown2html_safe(content: str):

    md = markdown.Markdown(extensions=[Yt2iframe()])
    html_unsafe = md.convert(content)
    print(html_unsafe)
    # set strip to true?
    html_safe = bleach.clean(html_unsafe, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, protocols=ALLOWED_PROTOCOLS,strip=True)
    print(html_safe)

    return html_safe
