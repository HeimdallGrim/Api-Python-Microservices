FROM python:3.11-alpine

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5009

#nom de l'image docker : fastapi

CMD ["python", "monapi.py"]

VOLUME [ "/app/data" ]

