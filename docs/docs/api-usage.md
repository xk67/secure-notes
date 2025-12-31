# API Usage

To list and create notes, a token is required

## `/api/token`

- Get personal access token
- Requires a verified account

```bash
$ curl -X POST http://localhost:8000/api/token \
-H "Content-Type: application/json" \
-d '{"username": "admin", "password" :"admin"}'
{"token":"2f665f25269996aa9fe4e830804451bd0979c36c"}
```

```bash
$ curl -X POST http://localhost:8000/api/token -d 'username=admin&password=admin'
{"token":"2f665f25269996aa9fe4e830804451bd0979c36c"}
```
