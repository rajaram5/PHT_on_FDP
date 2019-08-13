from rdflib import URIRef, Literal
from SPARQLWrapper import SPARQLWrapper, JSON
import os
import FDP_SPARQL_crawler_RR_version



# specify optional data use conditions at each FDP level
use_conditions = [[(None,
                    URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                    URIRef('http://www.re3data.org/schema/3-0#Repository')
                    )],
                  [(None,
                    URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                    URIRef('http://www.w3.org/ns/dcat#Catalog')
                    )],
                  [(None,
                    URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                    URIRef('http://www.w3.org/ns/dcat#Dataset')
                    ),
                   (None,
                    URIRef('http://purl.org/dc/terms/license'),
                    URIRef('http://purl.org/NET/rdflicense/MIT1.0')
                    ),
                   (None,
                    URIRef('http://www.w3.org/ns/dcat#theme'),
                    URIRef('http://dbpedia.org/resource/Disease_registry')
                    )],
                  [(None,
                    URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
                    URIRef('http://www.w3.org/ns/dcat#Distribution')
                    ),
                   (None,
                    URIRef('http://www.w3.org/ns/dcat#accessURL'),
                    None
                    ),
                   (None,
                    URIRef('http://www.w3.org/ns/dcat#mediaType'),
                   Literal('text/turtle'))
                   ]
                  ]


#Get fdp uri from node envir variable
fdp_uri = os.environ.get("DATABASE_URI")
if fdp_uri is None:
    fdp_uri = "http://136.243.4.200:8092/fdp"
else:
    fdp_uri = str(fdp_uri)

print("fdp_uri :" + fdp_uri)
# Init crawler
crawler = FDP_SPARQL_crawler_RR_version.FDP_SPARQL_crawler_RR_version()
# Get SPARQL endpoint matches the condition
sparql_endpoint = crawler.get_endpoint(URIRef(fdp_uri), use_conditions)



if sparql_endpoint:
    print("sparql_endpoint :" + sparql_endpoint)
    sparql = SPARQLWrapper(sparql_endpoint)

    # Run get patient count query
    query = open('get_patient_count.rq', 'r').read()
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(results)
    # Write query result to output file file
    with open('output.txt', 'w') as f:
        f.write(str(results))
else:
    print("No SPARQL endpoint found")
