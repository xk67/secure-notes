# API Usage

**Security Note:** This API is only safe to use if requests are made over HTTPS

## `/api/token`

- Get personal access token
- Requires a verified account

```bash
$ curl -X POST http://localhost:8000/api/token \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password" :"admin"}'
```

```bash
$ curl -X POST http://localhost:8000/api/token -d 'username=admin&password=admin'
```

## `/api/notes`

- Get personal and public notes
- Requires a personal access token

```bash
$ curl -X GET http://localhost:8000/api/notes -H 'Authorization: Token <TOKEN>'
```

## `/api/note/create`

- Create a Note
- Requires a personal access token
- JSON keys `title` and `content` are required (`private` defaults to `on`)

```bash
$ curl -X POST http://localhost:8000/api/note/create \
-H "Authorization: Token <TOKEN>" \ 
-H "Content-Type: application/json" \
-d '{"title":"test", "content":"# test", "privat":"off"}' 
```

```bash
$ curl -X POST http://localhost:8000/api/note/create \
-H "Authorization: Token <TOKEN>" \
-d 'title=test&content=# test&private=off'
```
