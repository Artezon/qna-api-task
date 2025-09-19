# QnA service

This is a Python web service application where you can ask questions and post answers to them!

Below are instructions to run it in Docker :)

### 1. Build Docker Image

```bash
docker compose build
```

### 2. Set environment variables

Create an .env file and set all the variables described in `.env.example`:
```bash
cp .env.example .env
```
Alternatively add them into `docker-compose.yml` or set variables in your shell.

### 3. Change port mapping

If you changed port in environment variable, you also need to change the port on the right in `docker-compose.yml` to match. Change the left port if you want the app to use a different external port (optional).

### 4. Prepare the database

Make sure the database exists and is accessible with provided credentials. If you just installed or updated the app, please double-check anything and run the migration script:
```bash
docker compose run qna_app alembic upgrade head
```

### 5. Start the Docker container

```bash
docker compose up -d
```

### 6. The app should be up and running ^-^

<br>

## Developer notes

### Database Migrations

Whenever you change your models (e.g. add a column), generate a new migration:
```bash
alembic revision --autogenerate -m "describe your change"
```
Then upgrade the database to the latest revision:
```bash
alembic upgrade head
```
