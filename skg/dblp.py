'''
Created on 2022-11-17

@author: wf
'''
from lodstorage.sparql import SPARQL
import rdflib
from skg.profiler import Profiler

class Dblp:
    """
    Schloss Dagstuhl Dblp computer science bibliography
    """
    
    def __init__(self,endpoint:str="https://qlever.cs.uni-freiburg.de/dblp"):
        """
        constructor
        
        Args:
            endpoint(str): the endpoint to use
        """
        self.endpoint=endpoint
        self.schema="https://dblp.org/rdf/schema"
        self.sparql=SPARQL(self.endpoint)
        
    def loadSchema(self,profile:bool=True):
        """
        load the schema
        """
        # https://stackoverflow.com/questions/56631109/how-to-parse-and-load-an-ontology-in-python
        profiler=Profiler("reading dblp schema")
        g = rdflib.Graph()
        g.parse (self.schema, format='application/rdf+xml')
        dblp = rdflib.Namespace('https://dblp.org/rdf/schema#')
        g.bind('dblp', dblp)
        query = """
        select distinct ?s ?p ?o 
        where { ?s ?p ?o}
        """
        count=0
        for row in g.query(query):
            count+=1
            print(row)
        if profile:
            profiler.time("for {count} triples")