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
        self.semscholar=SemanticScholar()
        
    def showResults(self,results):
        print(results.total)
        for result in results:
            print(result)
        pass
        
    def testGetPaper(self):
        """
        test getting a paper
        """
        doi="10.1007/978-3-030-49461-2"
        paper=self.semscholar.get_paper(doi)
        print(json.dumps(paper.raw_data,indent=2,default=str))
        pass
    
    def testSearchAuthor(self):
        """
        test author search
        """
        results=self.semscholar.sch.search_author("Tim Berners-Lee")
        self.showResults(results)
    
    def testSearchPaper(self):
        """
        test paper search
        """
        titles=["M. Agosti, C. Thanos (Eds). Post-proceedings of the First Italian Research Conference on Digital Library Management Systems (IRCDL 2005), Padova, 28th January, 2005. September 2005."]
        for title in titles:
            results=self.semscholar.sch.search_paper(title)
            self.showResults(results)
        