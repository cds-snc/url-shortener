# Migration commands

Create a new automatic migration: `alembic revision --autogenerate -m "create xyz table"`

Create a new migration: `alembic revision -m "create xyz table"`

Run all migrations: `alembic upgrade head`

Get current state: `alembic current`

Revert all migrations: `alembic downgrade base`

Revert last migration: `alembic downgrade -1` or `alembic downgrade {rev_sha}`
