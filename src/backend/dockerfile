FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && \
    apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libfontconfig1 \
    libx11-dev

COPY ./backend/ .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py", "--port", "8000", "--workers=5"]