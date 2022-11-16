'''
Created on 2022-11-16

@author: wf
'''
from tests.basetest import Basetest
from skg.wdsearch import WikidataSearch

class TestWikidataSearch(Basetest):
    """
    test the wikidata search
    """
    
    def test_wikidata_search(self):
        """
        """
        search="Tim Berners-Lee"
        wd=WikidataSearch()
        search_result=wd.search(search)
        self.assertTrue(len(search_result)>0)
        r1=search_result[0]
        self.assertEqual("Q80",r1["id"])
        pass