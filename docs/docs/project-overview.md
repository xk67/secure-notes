# Project Overview

## Team Members
Nils Breuer

## Used Technologies

### Django

The main framework for the backend and frontend

- Version `5.2.9`
- Actively maintained on [GitHub](https://github.com/django/django) and well documented
- Released under the BSD-3-Clause License
- Chosen because of its built-in [security features](https://docs.djangoproject.com/en/5.2/topics/security/) and its ease of use with Python

### Markdown

Python library for markdown to html translation

- Version `3.10`
- Well known and actively maintained on [Github](https://github.com/Python-Markdown/markdown)
- Released under the BSD-3-Clause License
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

### Django REST framework

Framework for building APIs in Django

- Version `3.16.1`
- Actively maintained on [GitHub](https://github.com/encode/django-rest-framework) and well documented
- Released under the BSD 3-Clause License
- Chosen for its seamless integration with the Django ecosystem and its built-in token authentication

### Bleach

Python library for HTML sanitization  

- Version `6.3.0`
- Actively maintained on [GitHub](https://github.com/mozilla/bleach) by the well known Mozilla team
- Released under the Apache 2.0 License
- Chosen for its easy to use integration and custom sanitization rules

### Selenium

A browser automation framework for testing

- Version `4.39.0`
- Actively maintained on [GitHub](https://github.com/SeleniumHQ/selenium) and well documented
- Released under the Apache 2.0 License
- Recommended by Django and easy integration in the Django test environment

### Cryptography

A package providing cryptographic recipes and primitives for Python

- Version `46.0.3`
- Actively maintained on [GitHub](https://github.com/pyca/cryptography) and well documented
- Released under the Apache 2.0 License
- Chosen for its security and easy integration in Python applications
