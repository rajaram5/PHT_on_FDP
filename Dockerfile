FROM python:3.7

#COPY requirements.txt /requirements.txt
COPY ./ /

RUN pip install -r requirements.txt

CMD ["python", "PatientCountTrain.py"]