from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# docker run --name fastrestproj-postgres -p 5538:5432 -e POSTGRES_PASSWORD=changeme -d postgres
# docker ps
# docker exec -it fastrestproj-postgres bash
# psql -h localhost -U postgres
# CREATE DATABASE fast_rest_proj; 
# DROP DATABASE fast_rest_proj; 
# \l    - list of databases


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:changeme@localhost:5538/fast_rest_proj"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()