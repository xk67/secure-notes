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

**Cross-Site Scripting (XSS)**

- **Potential vulnerability**:  
  The search query is reflected on the result page, which could theoretically be abused for XSS attacks if malicious input is provided.
- **Mitigation**:  
  Django’s template system automatically escapes user-supplied data by default, ensuring that special characters are rendered safely.

**SQL Injection**

- **Potential vulnerability**:  
  The query string is used to filter note titles in the database, which could raise concerns about SQL injection.
- **Mitigation**:  
  Django’s ORM protects against SQL injection by using query parameterization. SQL code and user-supplied parameters are handled separately and parameters are safely escaped.

### Data Protection

During the note search process no search queries or results are stored*.

\* For more information on data processing and user rights, refer to the Secure Notes data protection page.
