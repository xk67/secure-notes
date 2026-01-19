# secure-notes

Basic setup instructions for the development environment

This project provides two Docker Compose files:

- `compose.yml`: starts the app container on port 8000  
- `compose-docs.yml`: starts the app on port 8000 and the documentation on port 3000

Start the app using:

```bash
docker compose -f compose.yml up --build
```

Or start both app and docs using:

```bash
docker compose -f compose-docs.yml up --build
```

To ensure full functionality (such as registration verification emails or password resets), start a mail service like MailHog to receive emails sent by the app. Don’t forget to change the email IP in the env.dev file located in the src folder ;)
