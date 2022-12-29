'''
Created on 2022-11-16

@author: wf
'''
from skg.wikidata import Wikidata
from skg.dblp import Dblp
from lodstorage.sparql import SPARQL

class Concept:
    """
    an Entity
    """
    def __init__(self,name:str,cls):
        """
        constructor
        
        Args:
            name(str): the name of the node
            cls: a class
        """
        self.name=name
        self.props={}
        self.cls=cls
        if hasattr(cls,"getSamples"):
            for sample in cls.getSamples():
                for key in sample.keys():
                    if not key in self.props:
                        self.props[key]=Property(self,key)
                    
    def map(self,map_name:str,map_list:list):
        """
        map the given list of property mappings under the given map_name
        
        Args:
            map_name(str): the name of the mapping e.g. "wikidata"
            map_list(list): a list of mapping tuples
        """
        for prop_name,mapped_prop in map_list:
            if prop_name in self.props:
                prop=self.props[prop_name]
                prop.setmap(map_name,mapped_prop)
        return self
                    
    def map_wikidata(self,wd_class:str,scholia_suffix,map_list:list):
        """
        map wikidata entries
        
        Args:
            wd_class(str): the main wikidata base class
            scholia_suffix(str): the scholia suffix
        """
        self.wd_class=wd_class
        self.scholia_suffix=scholia_suffix
        self.map("wikidata",map_list)
        return self    
    
            
class Property:
    """
    a Property
    """
    def __init__(self,concept:Concept,name:str):
        """
        constructor
        
        Args:
            concept(Concept): the concept this property belongs to
            name(str): the name of the property
            
        """
        self.concept=concept
        self.name=name
        self.maps={}
        
    def setmap(self,map_name,mapped_prop):
        """
        map the given property
        """
        self.maps[map_name]=mapped_prop
        
    def getmap(self,map_name):
        return self.maps[map_name]
        
    def hasmap(self,map_name:str)->bool:
        """
        check whether there is a mapping for the given map_name
        
        Args:
            map_name(str): the map name to check
            
        Returns:
            bool: True if there is mapping
        """
        return map_name in self.maps
    
class Node:
    """
    a Node in the scholary knowledge graph
    """
    debug=False
    
    def __init__(self):
        """
        constructor
        """
    
    def __str__(self):
        """
        return a text representation of me
        """
        text=f"{self.concept.name} ➞ {self.label}:"
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
                
    def browser_url(self):
        """
        get my browser url
        """
        if self.provenance=="wikidata":
            url=self.scholia_url()
        else:
            url=self.label
        return url
                
    def scholia_url(self):
        """
        get my scholia url
        """
        prefix=f"https://scholia.toolforge.org/{self.concept.scholia_suffix}"
        wd_url=getattr(self, "wikiDataId",None)
        if wd_url is None:
            return None
        else:
            qid=wd_url.replace("http://www.wikidata.org/entity/","")
            return f"{prefix}/{qid}"
        
    @classmethod
    def setProvenance(cls,instances:list,provenance:str):
        """
        set the provenance of the given instances
        """
        for instance in instances:
            instance.provenance=provenance    
        
    @classmethod
    def from_sparql(cls,sparql:SPARQL,sparql_query:str,concept:Concept):
        """
        get instance from the given sparql access point with the given sparql_query for
        the given concept
        
        Args:
            sparql(SPARQL): the sparql access point
            sparql_query(str): the query to execute
            concept(Concept): the concept to create instances for
        """
        if Node.debug:
            print(sparql_query)
        records=sparql.queryAsListOfDicts(sparql_query)
        instances=cls.from_records(records,concept)
        return instances
        
    @classmethod
    def from_records(cls,records:list,concept:Concept):
        """
        get instances from the given records for the given concept
        
        Args:
            records(list): a list of dicts to get instances for
            concept(Concept): the concept to create instances for
        """
        instances=[]
        for record in records:
            # call my constructor
            instance=cls()
            instance.from_dict(concept,record)
            instances.append(instance)
        return instances
        
    @classmethod
    def from_wikidata_via_id(cls,concept:Concept,id_name:str,id_value:str,lang:str="en"):
        """
        get a node instance from wikidata for the given parameters
        
        Args:
            concept(Concept): the concept to return
            id_name(str): the name of the id to search / lookup with
            id_value(str): the value of the id
            lang(str): the language code to apply
        """
        wikidata=Wikidata()
        if id_name=="wikiDataId":
            value_clause=f"<http://www.wikidata.org/entity/{id_value}>"
        else:
            value_clause=f'''"{id_value}"'''
        sparql_query=f"""# Query for {concept.name} details via ID {id_name} value {id_value}
PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?{concept.name} ?qId"""
        for prop in concept.props.values():
            sparql_query+=f" ?{prop.name}"
        sparql_query+=f"""
WHERE {{
  VALUES ?{id_name} {{
    {value_clause}
  }}
  # classification!
  ?wikiDataId wdt:P31/wdt:P279* wd:{concept.wd_class}.
  ?wikiDataId rdfs:label ?{concept.name} .
  FILTER(LANG(?{concept.name})="{lang}").
"""
        for prop in concept.props.values():
            if prop.name=="wikiDataId":
                continue
            if not (prop.hasmap("wikidata")):
                raise Exception(f"Property {prop.name} of {concept.name} has no wikidata mapping")
            wd_prop=prop.getmap("wikidata")
            clause=f"?wikiDataId wdt:{wd_prop} ?{prop.name}."
            if prop.name!=id_name:
                clause=f"OPTIONAL {{ {clause} }}"
            sparql_query+="\n  "+clause
        sparql_query+="\n}"
        instances=cls.from_sparql(wikidata.sparql,sparql_query,concept)
        cls.setProvenance(instances, "wikidata")
        return instances
    
    
    @classmethod
    def from_dblp_via_id(cls,concept:Concept,id_name:str,id_value:str,lang:str="en"):
        """
        get a node instance from dblp for the given parameters
        
        Args:
            concept(Concept): the concept to return
            id_name(str): the name of the id to search / lookup with
            id_value(str): the value of the id
            lang(str): the language code to apply
        """
        dblp=Dblp()
        sparql_query=f"""
PREFIX dblp: <https://dblp.org/rdf/schema#>
SELECT 
  ?{concept.name}"""
        for prop in concept.props.values():
            if prop.hasmap("dblp"):
                sparql_query+=f" ?{prop.name}"
        if id_name=="doi":
            value_clause=f"<http://dx.doi.org/{id_value}>"
        elif id_name=="orcid":
            value_clause=f"<https://orcid.org/{id_value}>"
        else:
            value_clause=f'''"{id_value}"'''
        sparql_query+=f"""
WHERE {{
  VALUES ?{id_name} {{
    {value_clause}
  }}
"""
        for prop in concept.props.values():
            if prop.hasmap("dblp"):
                dblp_prop=prop.getmap("dblp")
                sparql_query+=f"""?{concept.name} dblp:{dblp_prop} ?{dblp_prop}.\n"""
        sparql_query+="}\n"
        instances=cls.from_sparql(dblp.sparql,sparql_query,concept)
        cls.setProvenance(instances, "dblp")
        return instances
        