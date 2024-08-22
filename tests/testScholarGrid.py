"""
Created on 2023-01-04

@author: wf
"""

from ez_wikidata.wbquery import WikibaseQuery
from ngwidgets.basetest import Basetest
from wikibot3rd.wikiuser import WikiUser

from skg.scholargrid import ScholarGrid, ScholarQuery
from skg.wikidata import Wikidata


class TestScholarGrid(Basetest):
    """
    test Scholar Grid behavior
    """

    def testScholarQuery(self):
        """
        test the Wikibase Query for Scholars
        """
        debug = True
        sq = ScholarQuery.get()
        self.assertIsNotNone(sq)
        self.assertTrue(isinstance(sq, WikibaseQuery))
        if debug:
            print(sq)

    def testGetScholars(self):
        """
        test getting scholars
        """
        wikiUsers = WikiUser.getWikiUsers()
        wikidata = Wikidata()
        sparql = wikidata.sparql
        for wikiId, expected in [("ceur-ws", 10), ("media", 500)]:
            if wikiId in wikiUsers:
                scholarGrid = ScholarGrid(
                    app=None, wikiUsers=wikiUsers, wikiId=wikiId, sparql=sparql
                )
                scholars = scholarGrid.getScholars()
                debug = self.debug
                debug = True
                if debug:
                    print(f"found {len(scholars)} scholars in {wikiId} wiki")
                self.assertTrue(len(scholars) > expected)
