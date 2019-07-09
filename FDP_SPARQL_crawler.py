import rdflib
from pprint import pprint
from rdflib import RDFS, URIRef, Literal
from SPARQLWrapper import SPARQLWrapper
import os

"""
TODO:
refactoring and testing
proper logging rather than stdout prints
generalize to other end-point type or other RDF distribution types

LIMITATIONS:
returns only a single end-point even if multiple are available
"""

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

def test_sparql_access(urls):
    """Return the first of the urls that gives a SPARQL response """
    sparql = SPARQLWrapper(str(urls[0]))
    sparql.setQuery("select * where {?s ?p ?o} limit 10")
    try:
        if 'application/sparql-results+xml' in sparql.query().info()['content-type']:
            print('found SPARQL end point ' + str(urls[0]))
            return str(urls[0])
    except:
        return None
    return None

def get_endpoint(url, route, conditions):
    """Apply a minimal set of FDP/DCAT semantics to crawl through a FDP and
    find and return any available SPARQL end-points."""
    g=rdflib.Graph()
    g.load(url)

    for c in conditions.pop(0):
        if len(list(g.triples(c))) == 0:
            print('mismatched condition')
            return

    route_predicate = route.pop(0)
    print("finding route using ", route_predicate, ":")
    leads = list(g.objects(None,URIRef(route_predicate)))
    print("leads:")
    pprint(leads)
    if len(route) == 0:
        if len(leads) > 0:
            return test_sparql_access(leads)
        return
    for i in leads:
        result = get_endpoint(i, route.copy(), conditions.copy())
        if result:
            return result

#print(get_endpoint(URIRef('https://demofdp1.fairdata.solutions/fdp'), fdp_route, use_conditions))

result = get_endpoint(URIRef('https://demofdp1.fairdata.solutions/fdp'), fdp_route, use_conditions)
print("DATABASE_URI : " + os.environ.get("DATABASE_URI"))
print("database_uri : " + os.environ.get("database_uri"))
print("endpointUrl : " + os.environ.get("endpointUrl"))
print(result)
# Write output to file
with open('output.txt', 'w') as f:
    f.write(result)
