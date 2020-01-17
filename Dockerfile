FROM python:3.5

WORKDIR /usr/src/app

#COPY requirements.txt /requirements.txt
COPY ./ /usr/src/app

RUN pip install -r  /usr/src/app/requirements.txt

CMD ["python", "/usr/src/app/FindDatasetTrain.py"]