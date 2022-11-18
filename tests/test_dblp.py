'''
Created on 2022-11-17

@author: wf
'''
from tests.basetest import Basetest
from skg.dblp import Dblp

class TestDblp(Basetest):
    """
    test dblp access
    """
    
    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.dblp=Dblp()
    
    def test_dblp(self):
        """
        test dblp access
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
        self.dblp.loadSchema(formats="n3,xml")
        