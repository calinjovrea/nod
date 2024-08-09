FROM ubuntu:latest

RUN apt update
RUN apt upgrade -y
RUN apt install -y python3-dev python3-pip 

COPY . .

RUN python3 -m pip install -r requirements.txt

# CMD python3 -m Registru.bloc 2>&1 && python3 -m pytest Registru/testări 2>&1
RUN python3 -m Registru.aplicație
