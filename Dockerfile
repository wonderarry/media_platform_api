FROM python:3.9.6

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD bash -c 'alembic upgrade head && uvicorn app.main:app --port 8008 --host 0.0.0.0'
#CMD ["uvicorn", "app.main:app", "--port", "8008", "--host", "0.0.0.0"]
