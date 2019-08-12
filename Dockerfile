FROM python:3.7

COPY requirements.txt /requirements.txt
COPY FDP_SPARQL_crawler.py /FDP_SPARQL_crawler.py

RUN pip install -r requirements.txt

CMD ["python", "PatientCountTrain.py"]