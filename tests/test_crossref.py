'''
Created on 2022-11-17

@author: wf
'''
from tests.basetest import Basetest
from skg.crossref import Crossref
import json
from dataclasses import dataclass

@dataclass
class Example:
    doi:str
    author:str
        
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
        debug=self.debug
        #debug=True
        doi_examples=[
            Example("10.1007/11581116_19","Atanas Kiryakov"),
            Example("10.1016/J.ARTMED.2017.07.002","Jean-Baptiste Lamy"),
            Example("10.1145/2882903.2899389","Rihan Hai")
        ]
        for example in doi_examples:
            doi=example.doi
            bib_entry=self.crossref.doiBibEntry(doi)
            if debug:
                print(bib_entry)
            expected=f"author = {{{example.author}"
            self.assertTrue(expected in bib_entry,expected)
            meta_data=self.crossref.doiMetaData(doi)
            if debug:
                print(json.dumps(meta_data,indent=2))
                self.assertTrue("DOI" in meta_data)
                self.assertEqual(doi.lower(),meta_data["DOI"])
                scite_entry=self.crossref.asScite(meta_data)
            if debug:
                print(scite_entry)

    def test_cookies(self):
        """
        test session cookies default
        """
        import requests
        session = requests.Session()
        cookie_dict=session.cookies.get_dict()
        if self.debug:
            print(session.cookies.get_dict())
        self.assertEqual({},cookie_dict)
        
