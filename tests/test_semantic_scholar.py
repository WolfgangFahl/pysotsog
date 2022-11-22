'''
Created on 2022-11-22

@author: wf
'''
from tests.basetest import Basetest
from skg.semantic_scholar import SemanticScholar
import json

class TestSemanticScholar(Basetest):
    """
    test Semantic Scholar Access
    """
    
    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.scholar=SemanticScholar()
        
    def testGetPaper(self):
        """
        test getting a paper
        """
        doi="10.1007/978-3-030-49461-2"
        paper=self.scholar.get_paper(doi)
        print(json.dumps(paper.raw_data,indent=2,default=str))
        pass