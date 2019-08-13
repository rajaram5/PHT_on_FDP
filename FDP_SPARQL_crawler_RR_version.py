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

class FDP_SPARQL_crawler_RR_version:

    gg = rdflib.Graph()


    def test_sparql_access(self, urls):
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



    def get_endpoint(self, url, route, conditions):
        """Apply a minimal set of FDP/DCAT semantics to crawl through a FDP and
        find and return any available SPARQL end-points."""

        gp = rdflib.Graph()
        self._load_graph(self.gg, url)

        if not self.is_graph_matches_condition(self.gg, conditions.pop(0)):
            return None

        for predicate in route:

            graphs = self._get_object_graphs(predicate)
            condition = conditions.pop(0)
            self.gg = rdflib.Graph()
            for g in graphs:
                if self.is_graph_matches_condition(g, condition):
                     self.gg =  self.gg + g

        for sub,pred,obj in self.gg.triples( (None,  URIRef('http://www.w3.org/ns/dcat#accessURL'), None) ):
            print ("%s is triplestore url "%obj)
            return obj




    def is_graph_matches_condition(self, graph, conditions):

        if conditions == []:
            return True

        for condition in conditions:
            c_list = list(graph.triples(condition))

            if len(c_list) == 0:
                print('mismatched condition')
                return False

        return True


    def _get_object_graphs(self, predicate):

        urls = list(self.gg.objects(None,URIRef(predicate)))

        graphs = []

        for url in urls:
            graph = rdflib.Graph()
            self._load_graph(graph, url)
            graphs.append(graph)
        return graphs

    def _load_graph(self, graph, url):
        print("Load content of : " + url)
        graph.load(url)




