"""
Steps to modify the ORM model:
1. Change python codes in this file.
2. In command line: $ alembic revision --autogenerate -m <message>
3. A file named <some hash>_<message>.py will appear at apis/alembic/versions
4. Check if the migration can work: $ alembic upgrade head
5. If no error, rollback: $ alembic downgrade -1
6. If with error, modify the file generated in step 3 then repeat step 4.
7. Add an API server version in migrate.py's VERSION array.
8. Add an alembic_upgrade() statement for that version, or add it in the ONLY_UPDATE_DB_MODELS array.
9. Commit all files includes the file generated in step 3 to git.
10. Restart the API server, then you're done.

If you don't have the alembic.ini, copy _alembic.ini and replace the postgres uri by yourself.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.get("SQLALCHEMY_DATABASE_URI"))
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AlembicVersion(Base):
    __tablename__ = "alembic_version"

    version_num = Column(String(32), primary_key=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
