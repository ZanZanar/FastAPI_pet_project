# make migrate msg="add something"
migrate:
	ENV=development PYTHONPATH=. alembic revision --autogenerate -m "$(msg)"

# make up
up:
	ENV=development PYTHONPATH=. alembic upgrade head
