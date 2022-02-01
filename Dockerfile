FROM python:3.10-alpine
WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

# Non project specific stuff
RUN apk update
RUN apk add git
COPY . /app
RUN git init -b master
RUN git remote add origin https://github.com/MrNavaStar/CountOnMe.git
RUN chmod +x update.sh

ENTRYPOINT ["python3", "bot/main.py"]