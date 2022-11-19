'''
Created on 2022-11-17

@author: wf
'''
from lodstorage.sparql import SPARQL
import rdflib
from rdflib.namespace import OWL
from skg.profiler import Profiler
import json

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
        self.schema_url="https://dblp.org/rdf/schema"
        self.sparql=SPARQL(self.endpoint)
        self.schema=None
        
    def show_triples(self,result):
        """
        show the triples for the given query result
        """
        for i,row in enumerate(result):
            print(f"{i+1}:{row}")
        
    def query_schema(self,query:str,formats:str="",profile:bool=False):
        """
        query the schema
        
        Args:
            query(str): the SPARQL query to execute
            formats(str): if "triples" is in th format string show the results string
            profile(bool): if True show timing information for the query
        """
        profiler=Profiler(f"query {query}")
        result=self.schema.query(query)
        if "triples" in formats:
            self.show_triples(result)
        if profile:
            profiler.time(f" for {len(result)} triples")
        return result
    
    def unprefix_value(self,value:object,prefixes:list=["http://xmlns.com/foaf/0.1/"])->str:
        """
        get rid of RDF prefixes to simplify our life
        
        Args:
            value(object): the RDFLib value to unprefix
            prefixes(list): list of prefixes to remove
        Returns:
            str: a simple string representation
        """
        if isinstance(value,list):
            if len(value)>=1:
                    value=value[0]
        if isinstance(value,dict):
            for akey in ["@id","@value"]:
                if akey in value:
                    value=value[akey]
        if isinstance(value,str):
            parts=value.split("#")
            if len(parts)==2:
                value=parts[1]
        for prefix in prefixes:
            if value.startswith(prefix):
                value=value.replace(prefix,"")
        return value
    
    def unprefix_row(self,row:dict):
        """
        get rid of the RDF prefixes in keys and values of the given row
        to simplify our life
        
        Args:
            row(dict): a dict of RDF values to unprefix
        """
        for key in list(row.keys()):
            org_value=row[key]
            value=self.unprefix_value(org_value)
            row[key]=value
            if "#" in key:
                noprefix_key=self.unprefix_value(key)
                row[noprefix_key] = row.pop(key)
            row[f"{key}_rdf"]=org_value
    
    def toPlantUml(self):
        """
        get a plantuml version of the schema
        """
        classes=self.toClasses()
        markup=""
        for cname,clazz in classes.items():
            class_markup=""
            for pname,prop in clazz.items():
                class_markup+=f"  {pname}\n"
            class_markup=f"class {cname}{{\n{class_markup}\n}}"
            markup+=class_markup
        return markup
        
    def toClasses(self):
        """
        convert to a classes dict of dicts
        
        Returns:
            dict: a dict of dictionaries
        """
        json_ld=self.schema.serialize(format="json-ld")
        schema_dict=json.loads(json_ld)
        classes={}
        # get rid of prefixes
        for row in schema_dict:
            self.unprefix_row(row)
        # pass 1 - classes
        for row in schema_dict:
            name=row["@id"]
            ptype=row["@type"]
            comment=row.get("comment","")
            label=row.get("label","")
            subClassOf=row.get("subClassOf","")
            if ptype=="Class":
                if name in classes:
                    clazz=classes[name]
                else:
                    clazz={
                        "@comment":comment,
                        "@label": label,
                        "@subClassOf": subClassOf
                    }
                    classes[name]=clazz
        # pass 2 - properties
        for row in schema_dict:
            name=row["@id"]
            ptype=row["@type"]
            comment=row.get("comment","")
            domain=row.get("domain","")
            prange=row.get("range","")
            plabel=row.get("label")
            if ptype=="Property":
                prop={
                    "name": name,
                    "comment": comment,
                    "label": plabel,
                    "domain": domain,
                    "range": prange
                }
                if domain in classes:
                    clazz=classes[domain]
                    clazz[name]=prop
            pass
        wrapped_classes={
            "classes":classes
        }
        return wrapped_classes
        
    def loadSchema(self,formats:str="n3",profile:bool=True):
        """
        load the schema
        """
        # https://stackoverflow.com/questions/56631109/how-to-parse-and-load-an-ontology-in-python
        profiler=Profiler("reading dblp schema")
        self.schema = rdflib.Graph()
        self.schema.parse (self.schema_url, format='application/rdf+xml')
        if profile:
            profiler.time(f" for {len(self.schema)} triples")
        for t_format in formats.split(","):
            if t_format!="triples":
                print (self.schema.serialize(format=t_format))
        dblp = rdflib.Namespace('https://dblp.org/rdf/')
        self.schema.bind('dblp', dblp)
        self.schema.bind('owl',OWL)
        query = """select distinct ?s ?p ?o 
where { ?s ?p ?o}
"""
        self.query_schema(query,formats=formats,profile=profile)
        return self.schema