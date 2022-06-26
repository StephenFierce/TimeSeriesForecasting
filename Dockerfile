#Specifying the base image
FROM python:3.9.12

EXPOSE 1883 1883

#install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#File to be run in docker
COPY main.py ./
COPY 2.json ./
COPY 3.json ./
COPY laadpalen.json ./

#Run file in our container terminal
CMD [ "python3","-u", "./main.py" ]