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
    
    
    def test_crossref(self):
        """
        test crossref
        """
        dois=["10.1016/J.ARTMED.2017.07.002"]
        crossref=Crossref()
        bib_entry=crossref.doiBibEntry(dois)
        print(bib_entry)
        meta_data=crossref.doiMetaData(dois)
        print(json.dumps(meta_data,indent=2))
