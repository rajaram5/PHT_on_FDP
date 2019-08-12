FROM python:3.7

WORKDIR /usr/src/app

#COPY requirements.txt /requirements.txt
COPY ./ /

RUN pip install -r requirements.txt

CMD ["python", "PatientCountTrain.py"]