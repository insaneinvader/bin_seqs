FROM python:3.11.3-slim-buster
WORKDIR /tmp
COPY requirements.txt .
RUN pip3 install -r requirements.txt
WORKDIR /app
# Remember to do: docker run -v .:/app
ENTRYPOINT ["python3", "app.py"]
