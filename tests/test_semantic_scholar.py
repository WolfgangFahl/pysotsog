"""
Created on 2022-11-22

@author: wf
"""

import json

from basemkit.basetest import Basetest

from skg.semantic_scholar import SemanticScholar


class TestSemanticScholar(Basetest):
    """
    test Semantic Scholar Access
    """

    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.semscholar = SemanticScholar()

    def showResults(self, results):
        print(results.total)
        for result in results:
            print(result)
        pass

    def testGetPaper(self):
        """
        test getting a paper
        """
        doi = "10.1007/978-3-030-49461-2"
        paper = self.semscholar.get_paper(doi)
        if self.debug:
            print(json.dumps(paper.raw_data, indent=2, default=str))
        pass

    def testSearchAuthor(self):
        """
        test author search
        """
        results = self.semscholar.sch.search_author("Tim Berners-Lee")
        self.showResults(results)

    def testSearchPaper(self):
        """
        test paper search
        """
        phrases = ["Get your own copy of wikidata"]
        for phrase in phrases:
            try:
                results = self.semscholar.sch.search_paper(phrase)
                self.showResults(results)
            except Exception as ex:
                print(f"exception on testSearchPaper: {str(ex)}")
                pass
