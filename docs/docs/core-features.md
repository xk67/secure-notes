# Core Features

## User Registration

### Technical Implementation

The registration is handled via a custom signup view that uses a custom form based on [UserCreationForm](https://github.com/django/django/blob/stable/5.2.x/django/contrib/auth/forms.py#L271).

HTTP POST request to `/signup` with the following application/x-www-form-urlencoded data:

  - `csrfmiddlewaretoken`
  - `username`
  - `email`
  - `password1`
  - `password2`

Data validation is handled by Django’s built-in validators:

**Username**:

  - [UnicodeUsernameValidator](https://github.com/django/django/blob/stable/5.2.x/django/contrib/auth/validators.py#L19) is used, enforcing a strict whitelist of allowed characters (letters, numbers, and @ . + - _ )
  - Must be unique among other users and has a maximum length of 150 characters ([User model](https://github.com/django/django/blob/stable/5.2.x/django/contrib/auth/models.py#L456))
  
**Email**: [EmailValidator](https://github.com/django/django/blob/stable/5.2.x/django/core/validators.py#L210) ensures a correctly formatted email address

**Password**:
  
  - [validate_password](https://github.com/django/django/blob/stable/5.2.x/django/contrib/auth/forms.py#L107) ensures `password1` matches `password2`
  - [validate_password](https://github.com/django/django/blob/main/django/contrib/auth/password_validation.py#L41) validates the password using the validators set in `AUTH_PASSWORD_VALIDATORS`:
    
    - `UserAttributeSimilarityValidator` checks similarity between the password and a set of user attributes
    - `MinimumLengthValidator` checks whether the password meets a minimum length
    - `CommonPasswordValidator` checks whether the password occurs in a list of common passwords (default list includes 20,000 passwords from [roycewilliams](https://gist.github.com/roycewilliams/226886fd01572964e1431ac8afc999ce))
    - `NumericPasswordValidator` checks whether the password is not entirely numeric
    - The implementation of the validators can be found [here](https://github.com/django/django/blob/stable/5.2.x/django/contrib/auth/password_validation.py)

  - **Password hashing**: Django uses [PBKDF2](https://github.com/django/django/blob/stable/5.2.x/django/contrib/auth/hashers.py#L311) with SHA256 by default. Each password is hashed with:
  
    - **Algorithm**: `pbkdf2_sha256`
    - **Iterations**: 1,000,000
    - **Salt**: randomly generated string via [get_random_string()](https://github.com/django/django/blob/stable/5.2.x/django/contrib/auth/hashers.py#L236) and unique per user
    
  - The password is stored as `<algorithm>$<iterations>$<salt>$<hash>` in the database
  - For more information on how Django handles passwords, see [Password Management in Django](https://docs.djangoproject.com/en/6.0/topics/auth/passwords/#password-management-in-django)

### Potential Vulnerabilities and Mitigations

**Username or Email Enumeration**

  - **Vulnerability**: An attacker could try to discover which usernames or email addresses are registered by observing error messages during registration.
  - **Mitigation**: Implemented a uniform error message: `"A user with the given email address or username already exists"` for both username and email conflicts, preventing enumeration.

**Weak Passwords**

  - **Vulnerability**: Users may choose passwords that are easy to guess or are included in common password lists
  - **Mitigation**: Enforced password validation using Django's validators:
    - Minimum length (default: 8 characters)
    - Not entirely numeric
    - Not included in the common passwords list
    - Not too similar to user attributes

**Cross-Site Request Forgery (CSRF)**

  - **Vulnerability**: Malicious sites could submit forms on behalf of a user
  - **Mitigation**: Django's CSRF middleware automatically protects the signup form

**Password Storage**

  - **Vulnerability**: Passwords stored in plaintext or using weak hashing could be exposed if the database is compromised
  - **Mitigation**: Django stores passwords securely using PBKDF2 with SHA256, unique per-user salt, and 1,000,000 iterations

**Input Sanitization / Injection**

  - **Vulnerability**: Unsanitized form input could lead to XSS or SQL injection.
  - **Mitigation**: Django forms automatically sanitize input and use parameterized queries through the ORM, preventing these attacks.

### Data Protection

During user registration, the following data is stored*:

- Username  
- Email address  
- Password (hashed)  
- Date joined  
- Last login  

## Note Search

The note search functionality is implemented via a custom `search_note` view that uses a custom form based on [Form](https://github.com/django/django/blob/stable/5.2.x/django/forms/forms.py#L432) class.

- An HTTP GET request is sent to `/search` with the query string parameter `q` as the search term
- The query string is used to search for notes whose title contains the provided search term
- The response consists of links to:
    - notes owned by the currently authenticated user and
    - public notes belonging to other users
- The query string is rendered on the result page as: `Results for: <q>`
- If no query string is provided or if the query length exceeds 32 characters an error message is shown to the user

### Potential Vulnerabilities and Mitigations

**Broken Access Control**

If access control checks are missing or incorrect, users could see
notes they do not own, including private notes of other users.

Mitigation: Use the ORM `filter()` function to ensure only public notes
are returned and `user.notes.all()` to include all notes owned by the
authenticated user.

**Cross-Site Scripting (XSS)**

The search query is reflected on the result page, which could theoretically
be abused if malicious input is provided.

Mitigation: Django’s template system automatically escapes user-supplied
data by default, ensuring special characters are rendered safely.

**SQL Injection**

The query string is used to filter note titles in the database, which could
raise concerns about SQL injection.

Mitigation: Use Django’s ORM and query parameterization to ensure that
SQL code and user-supplied parameters are handled separately and safely
escaped.

### Data Protection

During the note search process no search queries or results are stored*.

## Note Creation

### Technical Implementation
Note creation is handled via a custom
[`create_note`](https://github.com/xk67/secure-notes/blob/main/src/notes/views/web.py#L15)
view that uses a custom form based on  [ModelForm](https://docs.djangoproject.com/en/stable/topics/forms/modelforms/).

An HTTP **POST** request is sent to `/notes/create` with the following
`application/x-www-form-urlencoded` fields:

  - `csrfmiddlewaretoken`
  - `title`
  - `content`
  - `private`

[`Note`](https://github.com/xk67/secure-notes/blob/main/src/notes/models.py#L5)
model stores all note-related data. Django models define database schemas
using Python objects and are managed via Django’s ORM, for more information see [here](https://www.geeksforgeeks.org/python/django-orm-inserting-updating-deleting-data/).

The following columns are defined:

- `owner`: ForeignKey to `AUTH_USER_MODEL` with `on_delete=CASCADE`
- `title`: `CharField` with a maximum length of 32
- `content`: `TextField`
- `private`: `BooleanField` with a default value of `True`
- `uuid`: `UUIDField` with a unique identifier and a default value generated by the model

Before the **title** is inserted into the database, it is sanitized using
[`sanitize_title`](https://github.com/xk67/secure-notes/blob/main/src/notes/utils.py#L155).
Only plain text is allowed

The **content** is submitted by the user in Markdown format and processed
before being stored in the database as follows:

- [`markdown2html_safe`](https://github.com/xk67/secure-notes/blob/main/src/notes/utils.py#L147) is called, which:
- converts Markdown to HTML
- sanitizes the resulting HTML using predefined
    [`ALLOWED_TAGS`](https://github.com/xk67/secure-notes/blob/main/src/notes/utils.py#L11),
    [`ALLOWED_ATTRIBUTES`](https://github.com/xk67/secure-notes/blob/main/src/notes/utils.py#L33),
    and
    [`ALLOWED_PROTOCOLS`](https://github.com/xk67/secure-notes/blob/main/src/notes/utils.py#L9)

If the title or content is not submitted, the user receives an error
message generated by the custom
[`NoteForm`](https://github.com/xk67/secure-notes/blob/main/src/notes/forms.py#L5).

On success, the user is provided with a link to the newly created note in the form: `/notes/<uuid>`

### Potential Vulnerabilities and Mitigations

**SQL Injection**

User-controlled input (`title` and `content`) is written to the database during
note creation.

Django’s ORM mitigates SQL injection risks by using parameterized queries.
SQL statements and user-supplied values are handled separately, and all
parameters are safely escaped by default.

### Data Protection

During the note creation, the following personal data is stored:

- note owner
- note title
- note content
- note UUID

Users have the right to delete their notes at any time*.

## List Notes

### Technical Implementation
List notes is handled via a custom
[list_notes](https://github.com/xk67/secure-notes/blob/main/src/notes/views/web.py#L34)
view.

An simple HTTP **GET** request is sent to `/notes` and returns notes owned by the current user or other public notes.

### Potential Vulnerabilities and Mitigations

**Broken Access Control**

If access control checks are missing or incorrect, users could see
notes they do not own, including private notes of other users.

Mitigation: Use the ORM `filter()` function to return only public notes
and `user.notes.all()` to include all notes owned by the authenticated user.

**Cross-Site Scripting (XSS)**

The note title is reflected on the page, which could theoretically
be abused if malicious note title was set.

Mitigation: Use Django’s template system to automatically escape variables,
ensuring special characters are rendered safely. Note titles are also
sanitized at creation.

### Data Protection

During the list note process nothing is stored*.


\* For more information on data processing and user rights, refer to the Secure Notes data protection page.
