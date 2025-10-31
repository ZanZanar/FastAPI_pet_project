# make migrate msg="add something"
migrate:
	ENV=development PYTHONPATH=. alembic revision --autogenerate -m "$(msg)"

# make up
up:
	ENV=development PYTHONPATH=. alembic upgrade head


«Как запустить» и «Как тестировать»
## Run
```bash
env PYTHONPATH=. venv/bin/uvicorn fastapi_notes_api.app.main:app --reload
# http://127.0.0.1:8000/docs

Test
env PYTHONPATH=. ENV=test pytest -q