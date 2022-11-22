'''
Created on 2022-11-17

@author: wf
'''
from tests.base_skg_test import BaseSkgTest
from skg.dblp import Dblp
from skg.graph import Node
import json

class TestDblp(BaseSkgTest):
    """
    test dblp access
    """
    
    def setUp(self, debug=False, profile=True):
        BaseSkgTest.setUp(self, debug=debug, profile=profile)
        self.dblp=Dblp()
    
    def test_dblp_papers(self):
        """
        test dblp paper access
        """
        sparql_query="""
PREFIX dblp: <https://dblp.org/rdf/schema#>
SELECT 
  ?paper 
  (SAMPLE(?doi_o) as ?doi)
  (SAMPLE(?title_o) as ?title)
  (MIN(?year_o) as ?year)
  (GROUP_CONCAT(?author_o) as ?authors)
  (SAMPLE(?publishedin_o) as ?publishedin)
WHERE {
  ?paper dblp:title ?title_o .
  ?paper dblp:doi ?doi_o .
  ?paper dblp:authoredBy ?author_o.
  ?paper dblp:publishedIn ?publishedin_o .
  ?paper dblp:yearOfPublication ?year_o.
}
GROUP BY ?paper
ORDER BY DESC(?year)
LIMIT 10
        """
        # rows since the query above returns truly tabular results
        paper_rows=self.dblp.sparql.queryAsListOfDicts(sparql_query)
        debug=self.debug
        debug=True
        if debug:
            for row in paper_rows:
                print(row)
        
    def test_dblp_schema(self):
        """
        test loading the dblp schema
        """
        schema=self.dblp.schema
        schema.loadSchema(formats="n3,json-ld") # xml
        classes=schema.toClasses()
        debug=self.debug
        debug=True
        if debug:
            print(json.dumps(classes,indent=2))
        classes=classes["classes"]
        self.assertTrue("Entity" in classes)
        entity=classes["Entity"]
        self.assertTrue("@subClassOf" in entity)
        self.assertEqual("Thing",entity["@subClassOf"])
        
    def test_uml(self):
        """
        test getting uml markup
        """
        schema=self.dblp.schema
        schema.loadSchema()
        uml_markup=schema.toPlantUml()
        debug=True
        if debug:
            print(uml_markup)
            
    def test_dblp_item_via_id_search(self):
        """
        test getting papers by id from dblp
        """
        debug=self.debug
        debug=True
        paper_concept=self.skg_def.concepts["Paper"]
        author_concept=self.skg_def.concepts["Scholar"]
        id_examples=[
            {
                "id_name": "orcid",
                "id_value": "0000-0003-1279-3709",
                "concept": author_concept
            },
            {
                "id_name": "doi",
                "id_value": "10.1007/978-3-031-19433-7_21",
                "concept": paper_concept
            }
        ]
        
        def checkItem(item:Node,id_name:str,id_value:str,debug:bool=False):
            """
            check the given item
            
            Args:
                item(Node): the item to check
                id_name(str): the name of the id used to retrieve the item
                id_value(str) the value that has been used to retriebe the item
                debug(bool): if True show debug information
            """
            if id_name=="doi":
                self.assertEqual(f"http://dx.doi.org/{id_value}",item.doi)
        
        self.check_id_examples(id_examples, createFunc=Node.from_dblp_via_id,checkItem=checkItem,debug=debug)