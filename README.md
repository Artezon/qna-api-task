## Database Migrations

Whenever you change your models (e.g. add a column), generate a new migration:
```bash
alembic revision --autogenerate -m "describe your change"
```
Then upgrade the database to the latest revision:
```bash
alembic upgrade head
```
