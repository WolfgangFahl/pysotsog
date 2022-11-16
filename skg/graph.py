'''
Created on 2022-11-16

@author: wf
'''
from skg.wikidata import Wikidata

class Concept:
    """
    an Entity
    """
    def __init__(self,name:str,samples:list):
        """
        constructor
        
        Args:
            name(str): the name of the node
            samples(list): a list of dicts of sample values
        """
        self.name=name
        self.props={}
        for sample in samples:
            for key in sample.keys():
                if not key in self.props:
                    self.props[key]=Property(key)
                    
    def map_wikidata(self,wd_class:str,map_list:list):
        """
        map wikidata entries
        """
        self.wd_class=wd_class
        for prop_name,wd_prop in map_list:
            if prop_name in self.props:
                self.props[prop_name].wd_prop=wd_prop
            
class Property:
    """
    a Property
    """
    def __init__(self,name):
        self.name=name
    
class Node:
    """
    a Node in the scholary knowledge graph
    """
    
    def __init__(self):
        """
        constructor
        """
    
    def __str__(self):
        """
        return a text representation of me
        """
        text=f"{self.concept.name} {self.label}:"
        delim="\n  "
        for prop in self.concept.props.values():
            if hasattr(self, prop.name):
                text+=f"{delim}{prop.name}={getattr(self,prop.name)}"
        return text
        
    def from_dict(self,concept,record:str):
        """
        get my values from the given record
        """
        self.concept=concept
        self.label=record[concept.name]
        for key in concept.props.keys():
            if key in record:
                setattr(self, key, record[key])
        
    @classmethod
    def from_wikidata_via_id(cls,concept,id_name:str,id_value:str,lang:str="en"):
        wikidata=Wikidata()
        sparql_query=f"""# Query for {concept.name} details via ID {id_name} value {id_value}
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?{concept.name} ?qId"""
        for prop in concept.props.values():
            sparql_query+=f" ?{prop.name}"
        sparql_query+=f"""
WHERE {{
  VALUES ?{id_name} {{
    "{id_value}"
  }}
  ?wikiDataId wdt:P31 wd:{concept.wd_class}.
  ?wikiDataId rdfs:label ?{concept.name} .
  FILTER(LANG(?{concept.name})="{lang}").
"""
        for prop in concept.props.values():
            if prop.name=="wikiDataId":
                continue
            if not hasattr(prop, "wd_prop"):
                raise Exception(f"Property {prop.name} has no wikidata mapping")
            clause=f"?wikiDataId wdt:{prop.wd_prop} ?{prop.name}."
            if prop.name!=id_name:
                clause=f"OPTIONAL {{ {clause} }}"
            sparql_query+="\n  "+clause
        sparql_query+="\n}"
        records=wikidata.sparql.queryAsListOfDicts(sparql_query)
        instances=[]
        for record in records:
            instance=cls()
            instance.from_dict(concept,record)
            instances.append(instance)
        return instances