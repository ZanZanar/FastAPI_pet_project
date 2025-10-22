from sqlalchemy import create_engine
from fastapi_notes_api.app.models.model import Base

engine = create_engine("sqlite+pysqlite:///fastapi_notes_api/app/db/test.db",echo=True)

Base.metadata.create_all(engine)