FROM python:3.9.12
COPY . /usr/app/
EXPOSE 5096
WORKDIR /usr/app/
RUN pip install -r requirements.txt
RUN python3 -m pip install tensorflow-aarch64 -f /usr/app/tensorflow_aarch64-2.8.0-cp39-cp39-manylinux_2_17_aarch64.manylinux2014_aarch64.whl
#RUN python3 -m pip install tensorflow-aarch64 -f https://tf.kmtea.eu/whl/stable.html
CMD ["python3", "flask_api.py"]
