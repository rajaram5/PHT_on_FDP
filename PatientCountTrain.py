from rdflib import URIRef, Literal
from SPARQLWrapper import SPARQLWrapper, JSON
import os
import FDP_SPARQL_crawler

# FDP semantics (alternative implementation: crawl any link for dcat:Dataset)
fdp_route = ['http://www.re3data.org/schema/3-0#dataCatalog',
             'http://www.w3.org/ns/dcat#dataset',
             'http://www.w3.org/ns/dcat#distribution',
             'http://www.w3.org/ns/dcat#accessURL']

# specify optional data use conditions at each FDP level
use_conditions = [[],
                  [],
                  [(None,
                    URIRef('http://purl.org/dc/terms/license'),
                    URIRef('http://purl.org/NET/rdflicense/MIT1.0')),
                   (None,
                    URIRef('http://www.w3.org/ns/dcat#theme'),
                    URIRef('http://dbpedia.org/resource/Disease_registry'))
                   ],
                  [(None,
                    URIRef('http://www.w3.org/ns/dcat#mediaType'),
                    Literal('text/turtle'))]
                  ]


#Get fdp uri from node envir variable
fdp_uri = os.environ.get("DATABASE_URI")
if fdp_uri is None:
    fdp_uri = "http://136.243.4.200:8092/fdp"
else:
    fdp_uri = str(fdp_uri)

print("fdp_uri :" + fdp_uri)

sparql_endpoint = FDP_SPARQL_crawler.get_endpoint(URIRef(fdp_uri), fdp_route, use_conditions)

print("sparql_endpoint :" + sparql_endpoint)

if sparql_endpoint:
    print(sparql_endpoint)
    sparql = SPARQLWrapper(sparql_endpoint)
    query = open('get_patient_count.rq', 'r').read()
    print("query :" + query)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)
    # Write output to file
    with open('output.txt', 'w') as f:
        f.write(str(results))
