#Specifying the base image
FROM python:3.9.12

#install dependencies
RUN pip install tensorflow==2.7.0 -f https://tf.kmtea.eu/whl/stable.html
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#File to be run in docker
COPY LSTMModel.py ./

#Run file in our container terminal
CMD [ "python3", "./LSTMModel.py" ]