'''
Created on 2023-01-04

@author: wf
'''
from tests.basetest import Basetest
from skg.skgbrowser import SkgBrowser
from skg.scholargrid import ScholarGrid
from wikibot3rd.wikiuser import WikiUser

class TestScholarGrid(Basetest):
    """
    test Scholar Grid behavior
    """
    
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