FROM python:3.12-alpine

WORKDIR /app
RUN adduser -D app && chown -R app:app /app
USER app

COPY requirements.txt /app/
COPY main.py /app/

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]