import markdown
import bleach
#from django.utils.safestring import mark_safe

ALLOWED_TAGS = [
    'p', 'hr', #'br'
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'blockquote',
    'ul', 'ol', 'li',
    'pre', 'code',
    'a',
    'em', 'strong',
    'img'
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt']
}

#ALLOWED_PROTOCOLS: http, https, mailto

def markdown2html_safe(content: str):

    html_unsafe = markdown.markdown(content)
    # set strip to true?
    html_safe = bleach.clean(html_unsafe, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES,strip=True)
    print(html_safe)

    return html_safe
