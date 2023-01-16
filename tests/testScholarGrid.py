'''
Created on 2023-01-04

@author: wf
'''
from tests.basetest import Basetest
from skg.skgbrowser import SkgBrowser
from skg.scholargrid import ScholarGrid, ScholarQuery
from wikibot3rd.wikiuser import WikiUser
from spreadsheet.wbquery import WikibaseQuery

class TestScholarGrid(Basetest):
    """
    test Scholar Grid behavior
    """
    
    def testScholarQuery(self):
        """
        test the Wikibase Query for Scholars
        """
        debug=True
        sq=ScholarQuery.get()
        self.assertIsNotNone(sq)
        self.assertTrue(isinstance(sq,WikibaseQuery))
        if debug:
            print(sq)
    
    def testGetScholars(self):
        """
        test getting scholars
        """
        wikiUsers=WikiUser.getWikiUsers()
        for wikiId,expected in [("ceur-ws",10),("media",500)]:
            if wikiId in wikiUsers:
                scholarGrid=ScholarGrid(app=None,wikiUsers=wikiUsers,wikiId=wikiId)
                scholars=scholarGrid.getScholars()
                debug=self.debug
                debug=True
                if debug:
                    print(f"found {len(scholars)} scholars in {wikiId} wiki" )
                self.assertTrue(len(scholars)>expected)