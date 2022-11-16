'''
Created on 2022-11-16

@author: wf
'''
from tests.basetest import Basetest
from skg.wdsearch import WikidataSearch
from skg.wikidata import Wikidata
import json
from lodstorage.lod import LOD

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
        qids=["Q80","Q937","Q112055391"]
        expected=["Q5","Q5","Q52260246"]
        classes_map=wd.getClassQids(qids)
        if self.debug:
            print(json.dumps(classes_map,indent=2))
        for i,qid in enumerate(qids):
            classes=classes_map[qid]
            classes_by_class_qid,_dup=LOD.getLookup(classes, "class_qid")
            self.assertTrue(expected[i] in classes_by_class_qid)
            pass
