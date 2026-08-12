FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install flask mysql-connector-python

EXPOSE 5050

CMD ["python", "app.py"]