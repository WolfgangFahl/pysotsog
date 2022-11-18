'''
Created on 2022-11-17

@author: wf
'''
from lodstorage.sparql import SPARQL
import rdflib
from rdflib.namespace import OWL
from skg.profiler import Profiler

class Dblp:
    """
    Schloss Dagstuhl Dblp computer science bibliography
    """
    
    def __init__(self,endpoint:str="https://qlever.cs.uni-freiburg.de/api/dblp"):
        """
        constructor
        
        Args:
            endpoint(str): the endpoint to use
        """
        self.endpoint=endpoint
        self.schema="https://dblp.org/rdf/schema"
        self.sparql=SPARQL(self.endpoint)
        
    def loadSchema(self,formats:str="n3",profile:bool=True):
        """
        load the schema
        """
        # https://stackoverflow.com/questions/56631109/how-to-parse-and-load-an-ontology-in-python
        profiler=Profiler("reading dblp schema")
        g = rdflib.Graph()
        g.parse (self.schema, format='application/rdf+xml')
        dblp = rdflib.Namespace('https://dblp.org/rdf/')
        g.bind('dblp', dblp)
        g.bind('owl',OWL)
        query = """
        select distinct ?s ?p ?o 
        where { ?s ?p ?o}
        """
        count=0
        for row in g.query(query):
            count+=1
            if "triples" in formats:
                print(row)
        if profile:
            profiler.time(f"for {count} triples")
        for format in formats.split(","):
            if format!="triples":
                print (g.serialize(format=format))