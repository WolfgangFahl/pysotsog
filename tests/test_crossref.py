'''
Created on 2022-11-17

@author: wf
'''
from tests.basetest import Basetest
from skg.crossref import Crossref
import requests

class TestCrossref(Basetest):
    """
    test crossref access
    """
    
    def test_curl_style(self): 
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'curl/7.86.0',
            'Accept': 'application/x-bibtex',
        })
        from http.cookiejar import DefaultCookiePolicy
        session.cookies.set_policy(DefaultCookiePolicy(allowed_domains=[]))
        response=session.get('https://doi.org/10.1021/acs.jpcc.0c05161')
        print (response.status_code)
    
    def doi2bib(self,doi):
        """
        Return a bibTeX string of metadata for a given DOI.
        """
        url = f"https://doi.org/{doi}" 
        headers = {
            "accept": "application/x-bibtex"
        }
        r = requests.get(url, headers = headers)
        if r.status_code==200:
            return r.text
        else:
            return r.status_code
    
    def test_crossref_bib(self):
        doi="10.1016/J.ARTMED.2017.07.002"
        bib_text=self.doi2bib(doi)
        print (bib_text)
    
    def test_crossref_direct(self):
        """
        """
        headers = {
            'User-Agent': 'Mozilla/5.0; mailto:@doe.com',
        } 
        doi="10.1016/J.ARTMED.2017.07.002"
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
