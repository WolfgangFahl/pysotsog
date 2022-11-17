'''
Created on 2022-11-17

@author: wf
'''
from lodstorage.sparql import SPARQL

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