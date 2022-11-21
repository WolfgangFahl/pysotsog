'''
Created on 2022-11-17

@author: wf
'''
from tests.basetest import Basetest
from skg.crossref import Crossref
import json

class TestCrossref(Basetest):
    """
    test crossref access
    """
    
    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.crossref=Crossref()
    
    def test_crossref(self):
        """
        test crossref
        """
        from fake_useragent import UserAgent
        ua = UserAgent()
        ua.random
        debug=self.debug
        debug=True
        dois=["10.1016/J.ARTMED.2017.07.002"]
        bib_entry=self.crossref.doiBibEntry(dois)
        if debug:
            print(bib_entry)
        self.assertTrue("author = {Jean-Baptiste Lamy}," in bib_entry)
        meta_data=self.crossref.doiMetaData(dois)
        if debug:
            print(json.dumps(meta_data,indent=2))
        self.assertTrue("DOI" in meta_data)
        self.assertEqual(dois[0].lower(),meta_data["DOI"])
        scite_entry=self.crossref.asScite(meta_data)
        if debug:
            print(scite_entry)

    def test_cookies(self):
        """
        """
        import requests
        session = requests.Session()
        print(session.cookies.get_dict())
        
