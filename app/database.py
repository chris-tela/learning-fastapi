from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

#connects to database through SQLalchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# default values
SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine)

Base = declarative_base()

# session object creates a session with the database, letting us send SQL statements to it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#raw sql, not used by us
# while True:
#     try:
#         # to connect to SQL database
#         conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = '336005145', cursor_factory=RealDictCursor)
#         # cursor is used to execute SQL statements
#         cursor = conn.cursor()
#         print("Database connection was successful")
        
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print(error)
#         time.sleep(2)
