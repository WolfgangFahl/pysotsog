'''
Created on 2024-02-26

@author: wf
'''
from ngwidgets.basetest import Basetest
from skg.dblp2wikidata import Dblp2Wikidata
from argparse import Namespace

class TestDblp2Wikidata(Basetest):
    """
    test Dblp2Wikidata utility
    """

    def setUp(self, debug=True, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.d2w = Dblp2Wikidata(debug=debug)
    
    def test_transfer(self):
        """
        Test the transfer method for a known DBLP entry
        """
        test_search_terms=["82/6542","Donald C. Gause"]
        for test_search_term in test_search_terms:
            test_args = Namespace(dblp2wikidata=test_search_term)
            self.d2w.transfer(test_args)
        