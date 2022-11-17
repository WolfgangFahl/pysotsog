'''
Created on 2022-11-17

@author: wf
'''
from tests.basetest import Basetest
from skg.dblp import Dblp

class TestDblp(Basetest):
    """
    test dblp access
    """
    
    def test_dblp(self):
        """
        test dblp access
        """
        
    def test_dblp_ontology(self):
        """
        """
        dblp=Dblp()
        import logging
        import rdflib
        import time
        
        logging.basicConfig()
        logger = logging.getLogger('logger')
        logger.warning('The system may break down')
        
        start_time = time.time()
        
        g = rdflib.Graph()
        g.parse (dblp.schema, format='application/rdf+xml')
        #nif = rdflib.Namespace('http://purl.org/nif/ontology/nif.owl')
        #g.bind('nif', nif)
        query = """
        select distinct ?s ?p ?o 
        where { ?s ?p ?o}
        """
        count=0
        for row in g.query(query):
            count+=1
            print(row)
        elapsed=time.time() - start_time
        print(f"--- {elapsed} seconds for {count} triples---")