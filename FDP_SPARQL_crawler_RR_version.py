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

    # FDP semantics (alternative implementation: crawl any link for dcat:Dataset)
    fdp_route = ['http://www.re3data.org/schema/3-0#dataCatalog',
                 'http://www.w3.org/ns/dcat#dataset',
                 'http://www.w3.org/ns/dcat#distribution']


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



    def get_endpoint(self, url, conditions):
        """Apply a minimal set of FDP/DCAT semantics to crawl through a FDP and
        find and return any available SPARQL end-points."""

        # Load FDP content to graph
        self.gg = self._getGraph(url)

        # Check if fdp content mactches use condition, if not return None
        if not self._doesGraphMatchesCondition(self.gg, conditions.pop(0)):
            return None

        """
        Loop through FDP metadata layers to get triple store url
        """
        for predicate in self.fdp_route:
            # Get childern layers as graphs
            graphs = self._getObjectGraphs(predicate)
            condition = conditions.pop(0)

            # Empty gobal graph
            self.gg = rdflib.Graph()
            for g in graphs:
                if self._doesGraphMatchesCondition(g, condition):
                    # Add content of childern layer which matches use condition
                     self.gg =  self.gg + g
                else:
                    print('mismatched condition')

        """
        Get SPARQL endpoint url from the gobal graph. Note dat we written first SPARQL endpoint. In case of
        multiple endpoints URLs we ignore the rest
        """
        for sub, pred, obj in self.gg.triples( (None,  URIRef('http://www.w3.org/ns/dcat#accessURL'), None) ):
            return obj




    def _doesGraphMatchesCondition(self, graph, conditions):

        """
        Check if the content of the graph matches conditions. Return true if content matches conditions

        :param graph: RDF graph
        :param conditions: List of conditions
        :return:    True or False
        """

        if conditions == []:
            return True

        for condition in conditions:
            # Get triples matches condition
            c_list = list(graph.triples(condition))

            if len(c_list) == 0:
                return False
        return True


    def _getObjectGraphs(self, predicate):
        """
        For a given predicate get all objects of the predicate and load content of the object url(s) to graph(s).

        :param predicate: Predicate url
        :return:    List of graph(s)
        """
        urls = list(self.gg.objects(None,URIRef(predicate)))
        graphs = []

        for url in urls:
            graph = self._getGraph(url)
            graphs.append(graph)

        return graphs


    def _getGraph(self, url):
        """
        Load content of a url to graph

        :param url: Content url
        :return: Graph
        """
        print("Load content of : " + url)
        graph = rdflib.Graph()
        graph.load(url)
        return graph




