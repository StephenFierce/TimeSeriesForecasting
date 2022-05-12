#Specifying the base image
FROM armswdev/tensorflow-arm-neoverse:r22.05-tf-2.8.0-onednn-acl

#install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

#File to be run in docker
COPY LSTMModel.py ./
COPY /model ./


#Run file in our container terminal
#CMD [ "python3", "./LSTMModel.py" ]