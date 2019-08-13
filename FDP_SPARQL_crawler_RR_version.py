import rdflib
from pprint import pprint
from rdflib import RDFS, URIRef, Literal
from SPARQLWrapper import SPARQLWrapper

"""
TODO:
refactoring and testing
proper logging rather than stdout prints
generalize to other end-point type or other RDF distribution types

LIMITATIONS:
returns only a single end-point even if multiple are available
"""

# FDP semantics (alternative implementation: crawl any link for dcat:Dataset)
# fdp_route = ['http://www.re3data.org/schema/3-0#dataCatalog',
#              'http://www.w3.org/ns/dcat#dataset',
#              'http://www.w3.org/ns/dcat#distribution',
#              'http://www.w3.org/ns/dcat#accessURL']

# specify optional data use conditions at each FDP level
# use_conditions = [[],
#                   [],
#                   [(None,
#                     URIRef('http://purl.org/dc/terms/license'),
#                     URIRef('http://purl.org/NET/rdflicense/MIT1.0')),
#                     (None,
#                     URIRef('http://www.w3.org/ns/dcat#theme'),
#                     URIRef('http://dbpedia.org/resource/Disease_registry'))
#                   ],
#                   [(None,
#                     URIRef('http://www.w3.org/ns/dcat#mediaType'),
#                     Literal('text/turtle'))]
#                  ]

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
    _load_graph(g, url)

    for predicate in route:
        _load_object_content(g, predicate)

    for c in conditions:
        c_triples = g.triples(c)
        if len(c_triples) == 0:
            print('mismatched condition')
            return

    qres = g.query(
    """SELECT DISTINCT ?url
       WHERE {
          ?dist a  <http://www.w3.org/ns/dcat#Distribution>;

          ?a foaf:name ?aname .
          ?b foaf:name ?bname .
       }""")

#for row in qres:
#    print("%s knows %s" % row)



def _load_object_content(graph, predicate):

    urls = list(graph.objects(None,URIRef(predicate)))

    for url in urls:
        _load_graph(graph, url)

def _load_graph(graph, url):
    print("Load content of : " + url)
    graph.load(url)




