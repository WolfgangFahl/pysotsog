'''
Created on 2022-11-16

@author: wf
'''
from lodstorage.sparql import SPARQL
from lodstorage.lod import LOD
class Wikidata:
    """
    Wikidata access wrapper
    """
    def __init__(self,endpoint:str="https://query.wikidata.org/sparql",debug:bool=False):
        """
        constructor
        """
        self.endpoint=endpoint
        self.sparql = SPARQL(endpoint)
        self.debug=debug
        
        
    def getClassQids(self,qids:list)->dict:
        """
        get the Wikidata Q-Identifiers 
        for the given wikidata ids
        
        Args:
            qids(list): the list of id
        """
        sparql_query=f"""# get the instanceof values for a given entity
SELECT ?item ?itemLabel ?qid ?class_qid ?class ?classLabel
WHERE 
{{
  VALUES ?item {{
"""
        for qid in qids:
            if not qid.startswith("http:"):
                wd_url=f"http://www.wikidata.org/entity/{qid}"
            else:
                wd_url=qid
            sparql_query+=f"    <{wd_url}>\n"
        sparql_query+=f"""}}
  ?item wdt:P31/wdt:P279* ?class.
  ?item rdfs:label ?itemLabel
  FILTER(LANG(?itemLabel)="en")
  ?class rdfs:label ?classLabel
  FILTER(LANG(?classLabel)="en")
  BIND(REPLACE(STR(?class),"http://www.wikidata.org/entity/","") AS ?class_qid)
  BIND(REPLACE(STR(?item),"http://www.wikidata.org/entity/","") AS ?qid)
}}"""
        if self.debug:
            print(sparql_query)
        class_rows=self.sparql.queryAsListOfDicts(sparql_query)
        class_map=LOD.getLookup(class_rows, "qid", withDuplicates=True)
        return class_map
