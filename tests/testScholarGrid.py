'''
Created on 2023-01-04

@author: wf
'''
from tests.basetest import Basetest
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
        if "ceur-ws" in wikiUsers:
            scholarGrid=ScholarGrid(app=None,wikiUsers=wikiUsers,wikiId="ceur-ws")
            scholars=scholarGrid.getScholars()
            debug=self.debug
            debug=True
            if debug:
                print(f"found {len(scholars)} scholars")
            self.assertTrue(len(scholars)>10)
        
        