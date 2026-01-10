# Project Overview

## Team Members
Nils Breuer

## Used Technologies

### Django

The main framework for the backend and frontend

- Version `5.2.9`
- Actively maintained on [GitHub](https://github.com/django/django) and well documented
- It is released under the BSD-3-Clause License
- Chosen because of its built-in [security features](https://docs.djangoproject.com/en/6.0/topics/security/) and its ease of use with Python

### Markdown

Python library for markdown to html translation

- Version `3.10`
- Well known and actively maintained on [Github](https://github.com/Python-Markdown/markdown)
- It is released under the BSD-3-Clause License
- Chosen because of its easy extensibility, allowing the markdown interpreter to be extended with a custom extension for the social plugin

### Django-environ

Python library for reading environment variables in Django projects with type casting and validation

- Version `0.12.0`
- Not currently actively maintained, see [GitHub](https://github.com/joke2k/django-environ)
- Why this is not an issue for this project:
    - There are no dependencies that need frequent updates
    - No relevant security issues or open pull requests
    - It is just a library to read environment variables from a file at Django startup
- Released under the MIT License
- Chosen because of its automatic type casting and validation of read variables
