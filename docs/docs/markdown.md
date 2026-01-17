# Markdown Features

The following code block shows all the Markdown features implemented by this app

```markdown
# H1
## H2
### H3
#### H4
##### H5
###### H6

Header Level 1
===============

Header Level 2
---------------

---

This is a normal paragraph.
This line ends with two spaces to force a line break.

This is another paragraph after a blank line.

---

*Italic (asterisk)*
_Italic (underscore)_

**Bold (asterisk)**
__Bold (underscore)__

***Bold + Italic***
___Bold + Italic___

---

> This is a blockquote.
>
> It can span multiple paragraphs.
>
> > Nested blockquote.

---

* Item A
* Item B
    * Nested item B1
    * Nested item B2
- Item C
+ Item D

---

1. First item
2. Second item
    * Unordered sub-item
    * Another sub-item
3. Third item

---

Use the `printf()` function.

    def hello():
        print("Hello, world")

---

* * *

***

- - -

---

[Example](https://example.com/)

[Link with title](https://example.com/ "Example Title")

This is a [reference link][id].

[id]: https://example.com/ "Optional Title"

---

![Alt text](https://static.djangoproject.com/img/icon-touch.e4872c4da341.png "Optional title")

![Reference image][img]

[img]: https://static.djangoproject.com/img/icon-touch.e4872c4da341.png "Placeholder Image"

---

<https://example.com>
<email@example.com>

---

\*Not italic\*
\# Not a header
\> Not a blockquote

Escaped characters:

\` \* \_ \{ \} \[ \] \( \) \# \+ \- \. \!

---

<div>
  <strong>HTML inside Markdown</strong>
</div>

<p>This paragraph is written in HTML.</p>

This is <em>inline HTML</em> inside a paragraph.

---

Copyright symbol: &copy;
Non-breaking space: &nbsp;
Less than: &lt;
Greater than: &gt;

---

![youtu.be](embed:https://youtu.be/aHTCawFKkkw)

![youtube.com](embed:https://youtube.com/watch?v=aHTCawFKkkw)

![www.youtu.be](embed:https://www.youtu.be/aHTCawFKkkw)

![www.youtube.com](embed:https://www.youtube.com/watch?v=aHTCawFKkkw)

```

## Social Plugin

Embed YouTube videos via Markdown syntax

- **Syntax:** `![<Optional Title>](embed:<Link>)`
- Supported link formats:
    - `youtu.be/video_id`
    - `www.youtu.be/video_id`
    - `youtube.com/watch?v=video_id`
    - `www.youtube.com/watch?v=video_id`
- YouTube videos are embedded via an iframe, converted to `www.youtube-nocookie.com/embed/video_id`
- Users are asked for consent before the iframe loads
