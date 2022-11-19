'''
Created on 2022-11-17

@author: wf
'''
from tests.basetest import Basetest
from skg.dblp import Dblp
from skg.kg import SKG_Def
from skg.graph import Node
import json

class TestDblp(Basetest):
    """
    test dblp access
    """
    
    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
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
        self.dblp.loadSchema(formats="n3,json-ld") # xml
        classes=self.dblp.toClasses()
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
        self.dblp.loadSchema()
        uml_markup=self.dblp.toPlantUml()
        debug=True
        if debug:
            print(uml_markup)
            
    def test_dblp_item_via_id_search(self):
        """
        test getting papers by id from dblp
        """
        debug=self.debug
        debug=True
        skg_def=SKG_Def()
        paper_concept=skg_def.concepts["Paper"]
        author_concept=skg_def.concepts["Scholar"]
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
       
        for id_example in id_examples:
            id_name=id_example["id_name"]
            id_value=id_example["id_value"]
            id_concept=id_example["concept"]
            items=Node.from_dblp_via_id(id_concept,id_name,id_value)
            if debug:
                for item in items:
                    print(item)
            self.assertEqual(1,len(items))
            item=items[0]
            self.assertEqual(item.concept.name,id_concept.name)
            if id_name=="doi":
                self.assertEqual(f"http://dx.doi.org/{id_value}",item.doi)