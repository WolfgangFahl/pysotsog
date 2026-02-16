"""
Created on 2022-11-16

@author: wf
"""

import json
import unittest

from basemkit.basetest import Basetest
from lodstorage.lod import LOD

from skg.wdsearch import WikidataSearch
from skg.wikidata import Wikidata


class TestWikidataSearch(Basetest):
    """
    test the wikidata search
    """

    @unittest.skipIf(Basetest.inPublicCI(), "unreliable in public CI")
    def test_wikidata_search(self):
        """
        test the wikidata serarch API
        """
        searches = [("Tim Berners-Lee", "Q80"), ("Q950635", "Q950635")]
        wd = WikidataSearch()
        debug = self.debug
        debug = True
        for search, expected in searches:
            search_options = wd.searchOptions(search)
            self.assertTrue(len(search_options) > 0)
            qid, itemLabel, _desc = search_options[0]
            if debug:
                print(f"{qid}:{itemLabel}")
            self.assertEqual(expected, qid)
        pass

    def test_item_instanceof(self):
        """
        test getting the classes Q-Identifiers of a given instance
        """
        wd = Wikidata()
        qids = ["Q80", "Q937", "Q112055391"]
        expected = ["Q5", "Q5", "Q52260246"]
        classes_map = wd.getClassQids(qids)
        if self.debug:
            print(json.dumps(classes_map, indent=2))
        for i, qid in enumerate(qids):
            classes = classes_map[qid]
            classes_by_class_qid, _dup = LOD.getLookup(classes, "class_qid")
            self.assertTrue(expected[i] in classes_by_class_qid)
            pass
