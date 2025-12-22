import markdown

def markdown2html_safe(mardown: str):
    return markdown.markdown(mardown)
