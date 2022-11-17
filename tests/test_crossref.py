'''
Created on 2022-11-17

@author: wf
'''
from tests.basetest import Basetest
from skg.crossref import Crossref

class TestCrossref(Basetest):
    """
    test crossref access
    """
    
    def doi2bib(self,doi):
        """
        Return a bibTeX string of metadata for a given DOI.
        """
        import requests
    
        url = "https://dx.doi.org/" + doi
        
        headers = {
            "accept": "application/x-bibtex"
        }
        r = requests.get(url, headers = headers)
        
        return r.text
    
    def test_crossref_bib(self):
        return
        doi="10.1016/J.ARTMED.2017.07.002"
        bib_text=self.doi2bib(doi)
        print (bib_text)
    
    def test_crossref_direct(self):
        import requests
        import json
        headers = {
            'User-Agent': 'Mozilla/5.0; mailto:wf@bitplan.com',
        } 
        doi="10.13140/RG.2.2.14679.42409"
        url=f"https://api.crossref.org/v1/works/{doi}"
        print (url)
        response = requests.get(url,headers=headers)
        print(response.status_code)
        if response.status_code==200:
            print(response.json())
    
    def test_crossref(self):
        """
        test crossref
        """
        return
        dois=["10.1016/J.ARTMED.2017.07.002"]
        crossref=Crossref()
        #bib_entry=crossref.doiBibEntry(doi)
        meta_data=crossref.doiMetaData(dois)
        print(meta_data)
