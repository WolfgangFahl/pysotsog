'''
Created on 2022-11-16

@author: wf
'''
from tests.basetest import Basetest
from skg.wdsearch import WikidataSearch
from skg.wikidata import Wikidata

class TestWikidataSearch(Basetest):
    """
    test the wikidata search
    """
    
    def test_wikidata_search(self):
        """
        test the wikidata serarch API
        """
        search="Tim Berners-Lee"
        wd=WikidataSearch()
        search_options=wd.searchOptions(search)
        self.assertTrue(len(search_options)>0)
        qid,_itemLabel,_desc=search_options[0]
        self.assertEqual("Q80",qid)
        pass
    
    def test_item_instanceof(self):
        """
        test getting the classes Q-Identifiers of a given instance 
        """
        wd=Wikidata()
        classes_map=wd.getClassQids(["Q80","Q937"])
        print(classes_map)
        
