'''
Created on 2022-11-16

@author: wf
'''
from lodstorage.sparql import SPARQL
class Wikidata:
    """
    Wikidata access wrapper
    """
    def __init__(self,endpoint:str="https://query.wikidata.org/sparql"):
        """
        constructor
        """
        self.endpoint=endpoint
        self.sparql = SPARQL(endpoint)
        
class Property:
    """
    """
