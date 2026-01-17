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
