import markdown
import bleach
import re
from urllib.parse import urlparse, parse_qs
from markdown.extensions import Extension
from markdown.inlinepatterns import InlineProcessor
import xml.etree.ElementTree as etree

ALLOWED_PROTOCOLS = {'http', 'https', 'mailto'}

ALLOWED_TAGS = [
    'p', 'hr', 'br',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'blockquote',
    'ul', 'ol', 'li',
    'pre', 'code',
    'a',
    'em', 'strong',
    'img', 'iframe',
    # Consent wrapper elements
    'div', 'button', 'template',
    'section', 'header', 'article', 'footer',
    'span', 'mark', 'del', 'ins', 'sub', 'sup', 'small',
    'table', 'caption', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td',
    'figure', 'figcaption'
]

def iframe_attribute_filter(tag, name, value):
    if name == 'src':
        return value.startswith('https://www.youtube-nocookie.com/embed/')
    return name in ['title', 'referrerpolicy', 'frameborder', 'allowfullscreen']

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'img': ['src', 'alt', 'title'],
    'iframe': iframe_attribute_filter,
    'div': ['class']
}

EMBED_RE = r'!\[([^\]]*)\]\(embed:([^)]+)\)'

def extract_youtube_video_id(url: str) -> str | None:

    try:
        parsed = urlparse(url.strip())

        if parsed.scheme not in ('http', 'https'):
            return None

        hostname = parsed.hostname
        if not hostname:
            return None

        if hostname not in ('youtube.com', 'www.youtube.com', 'youtu.be', 'www.youtu.be'):
            return None

        video_id = None

        # Handle youtu.be/video_id
        if hostname in ('youtu.be', 'www.youtu.be'):
            path_parts = parsed.path.strip('/').split('/')
            if path_parts and path_parts[0]:
                video_id = path_parts[0]

        # Handle youtube.com/watch?v=video_id
        elif hostname in ('youtube.com', 'www.youtube.com'):
            if parsed.path.startswith('/watch'):
                query_params = parse_qs(parsed.query)
                if 'v' in query_params and query_params['v']:
                    video_id = query_params['v'][0]

        if video_id:
            video_id = video_id.split('?')[0].split('&')[0].split('/')[0]

            if re.match(r'^[a-zA-Z0-9_-]{10}[AEIMQUYcgkosw048]', video_id):
                return video_id

        return None

    except Exception:
        return None


def convert_to_youtube_nocookie_embed(url: str) -> str | None:

    video_id = extract_youtube_video_id(url)

    if not video_id:
        return None

    return f"https://www.youtube-nocookie.com/embed/{video_id}"

class EmbedInlineProcessor(InlineProcessor):
    def handleMatch(self, m, data):
        title = m.group(1)
        url = m.group(2)

        wrapper = etree.Element("div")
        wrapper.set("class", "embed-consent")

        etree.SubElement(wrapper, "p").text = "Allow content from YouTube?"

        p2 = etree.SubElement(wrapper, "p")
        p2.text = "This page contains content provided by YouTube. We ask for your consent before loading the content, as it may use cookies and other technologies. You should read "

        privacy_link = etree.SubElement(p2, "a")
        privacy_link.set("href", "https://policies.google.com/privacy")
        privacy_link.text = "YouTube's privacy policy"
        privacy_link.tail = " and "

        cookie_link = etree.SubElement(p2, "a")
        cookie_link.set("href", "https://policies.google.com/technologies/cookies")
        cookie_link.text = "cookie policy"
        cookie_link.tail = " before giving your consent."


        button = etree.SubElement(wrapper, "button")
        button.set("type", "button")
        button.text = "Accept and load content"

        template = etree.SubElement(wrapper, "template")

        embed_url = convert_to_youtube_nocookie_embed(url)

        if not embed_url:
            return None, None, None

        iframe = etree.SubElement(template, "iframe")
        iframe.set("src", embed_url)
        iframe.set("referrerpolicy", "strict-origin-when-cross-origin")
        iframe.set("frameborder", "0")
        iframe.set("allowfullscreen", "true")

        if title:
            iframe.set("title", title)

        return wrapper, m.start(0), m.end(0)

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
    html_safe = bleach.clean(html_unsafe, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, protocols=ALLOWED_PROTOCOLS,strip=True)

    return html_safe

def sanitize_title(title: str):
    return bleach.clean(title, strip=True)
