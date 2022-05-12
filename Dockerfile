#Specifying the base image
FROM python:3.9.12

#install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#File to be run in docker
COPY main.py ./

#Run file in our container terminal
CMD [ "python3", "./main.py" ]