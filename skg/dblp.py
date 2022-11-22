'''
Created on 2022-11-17

@author: wf
'''
from lodstorage.sparql import SPARQL
from skg.owl import Owl

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
        self.schema=Owl("dblp","https://dblp.org/rdf/schema", "Wolfgang Fahl","2022-11-19")
        self.sparql=SPARQL(self.endpoint)
        
    
    def get_paper_records(self,regex:str,prop_name:str="title",limit:int=100)->list:
        """
        get papers fitting the given regex
        
        Args:
            prop_name(str): the property to filter
            regex(str): the regex to filter for
            limit(int): the maximum number of records to return
            
        Returns:
            list: a list of dict of paper records
        """
        sparql_query="""PREFIX dblp: <https://dblp.org/rdf/schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT
  ?paper 
  ?year
  ?yearofevent
  #?month
  ?doi
  ?isbn
  ?title
  (GROUP_CONCAT(?author_o) as ?authors)
  ?publishedin
WHERE {
  ?paper dblp:title ?title .
  ?paper dblp:doi ?doi .
  OPTIONAL { ?paper dblp:yearOfEvent ?yearofevent } .
  OPTIONAL { ?paper dblp:isbn ?isbn }.
  ?paper dblp:authoredBy ?author_o.
  ?paper dblp:publishedIn ?publishedin .
  ?paper dblp:yearOfPublication ?year.
  OPTIONAL { ?paper dblp:monthOfPublication ?month}.
"""
        sparql_query+=f"""FILTER regex(?{prop_name}, "{regex}").\n"""
        sparql_query+=f"""
}}
GROUP BY 
  ?paper 
  ?title 
  ?doi 
  ?isbn
  ?year 
  ?yearofevent
  ?month 
  ?publishedin 
ORDER BY DESC(?year)
LIMIT {limit}"""
        records=self.sparql.queryAsListOfDicts(sparql_query)
        return records