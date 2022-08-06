from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sql_alch_url = """postgresql://postgres:123@localhost/fastapi_db"""
engine = create_engine(sql_alch_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# missed_attempts = 0
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi_db',
#                                 user='postgres', password='123', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('successfully connected to db')
#         break
#     except Exception as e:
#         missed_attempts += 1
#         print('conencting to db failed, error = ', e)
#         time.sleep(min(missed_attempts ** 2, 30))
