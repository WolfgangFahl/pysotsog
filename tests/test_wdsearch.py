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
        search_options=wd.searchOptions(search)
        self.assertTrue(len(search_options)>0)
        qid,_itemLabel,_desc=search_options[0]
        self.assertEqual("Q80",qid)
        pass