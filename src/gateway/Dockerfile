FROM python:3.12-slim


WORKDIR /gateway

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
