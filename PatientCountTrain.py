from rdflib import URIRef, Literal
from SPARQLWrapper import SPARQLWrapper, JSON
import os
import requests
import rdflib


#Get fdp uri from node envir variable
station_uri = os.environ.get("DATABASE_URI")
if station_uri is None:
    station_uri = "http://127.0.0.1:5000"
else:
    station_uri = str(station_uri)

print("station_uri :" + station_uri)

# Read train requirement
train_metadata = open('train-metadata.ttl', 'r').read()

# Get SPARQL endpoint matches the condition
url = station_uri + "/getDataAccessInterface"
response = requests.post(url,data = train_metadata)

print("content:"+ str(response.text))
sparql_endpoint = None
output = "No SPARQL endpoint found"

if response.text and response.status_code == 200:
    graph = rdflib.Graph()
    graph.parse(data=response.text, format="text/turtle")
    # Get triples store url
    for sub, pred, obj in graph.triples( (None,  URIRef('http://www.w3.org/ns/dcat#accessURL'), None) ):
        sparql_endpoint = str(obj)
        break;
    output = response.text



if sparql_endpoint:
    print("sparql_endpoint :" + sparql_endpoint)
    sparql = SPARQLWrapper(sparql_endpoint)

    # Run get patient count query
    query = open('get_patient_count.rq', 'r').read()
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    output = sparql.query().convert()

print(output)
# Write query result to output file file
with open('output.txt', 'w') as f:
    f.write(str(output))

