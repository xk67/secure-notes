# API Usage

**Security Note:** This API is only safe to use if requests are made over HTTPS.

## `/api/token`

- Get personal access token
- Requires a verified account
- Returns a JSON response containing the token and its expiry time
- By default, the token is valid for 10 hours. For more information see [here](https://github.com/jazzband/django-rest-knox/blob/develop/docs/settings.md)

```bash
curl -X POST http://localhost:8000/api/token \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password" :"admin"}'
```

```bash
curl -X POST http://localhost:8000/api/token -d 'username=admin&password=admin'
```

## `/api/notes`

- Get personal and public notes
- Requires a personal access token
- Returns a JSON array containing all private and public notes with title, content, and UUID


```bash
curl -X GET http://localhost:8000/api/notes -H 'Authorization: Token <TOKEN>'
```

## `/api/note/create`

- Create a Note
- Requires a personal access token
- JSON keys `title` and `content` are required (`private` defaults to `on`)
- Returns a JSON containing the UUID of the created note

```bash
curl -X POST http://localhost:8000/api/note/create \
-H "Authorization: Token <TOKEN>" \
-H "Content-Type: application/json" \
-d '{"title":"test", "content":"# test", "private":"off"}'
```

```bash
curl -X POST http://localhost:8000/api/note/create \
-H "Authorization: Token <TOKEN>" \
-d 'title=test&content=# test&private=off'
```

## `/api/note/<UUID>`

- Retrieve the content of a specific note by its UUID
- Requires a personal access token
- Returns a JSON with the note content

```bash
curl -X GET http://localhost:8000/api/note/<UUID> -H "Authorization: Token <TOKEN>"
```

## Technical Implementation

All API endpoints are implemented as Django REST Framework (DRF) API views.
Each view is protected with the following decorators:

```python
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
```

The APILoginView is used to generate personal access tokens. Tokens are stored
server-side in the database (knox_authtoken table) with the following fields:

- `digest`: a secure hash of the full token stored as the primary key. Knox uses a strong hash algorithm: SHA‑512. 
- `token_key`: the prefix or portion of the token stored for indexed lookup
- `user_id`: reference to the `auth_user` table indicating the token’s owner.
- `created`: timestamp for when the token was created.
- `expiry`: expiration datetime after which the token is no longer valid.

Custom [Serializers](https://github.com/xk67/secure-notes/blob/main/src/notes/serializers.py)
handle JSON input and output. If required fields are missing or invalid, the serializer
returns an error response to the user.

## Potential Vulnerabilities and Mitigations

**Unauthorized Access**

If token authentication is not enforced, private notes could be exposed.

Mitigation: All API views require a valid personal access token via
TokenAuthentication and IsAuthenticated permission class.

**Injection**

User-supplied JSON (title, content, private) could be invalid or
malicious.

Mitigation: DRF serializers validate input and reject requests missing
required fields or with invalid types.

**Broken Access Control**

If access control is missing, users could access
others’ private notes.

Mitigation: Each note view checks ownership or public status, and only
returns data the authenticated user is allowed to see.

## Data Protection

Generated tokens are securely stored, and any notes created via the API are saved*.

\* For more information on data processing and user rights, refer to the Secure Notes data protection page.
