'''
Created on 2022-11-22

@author: wf
'''
from tests.basetest import Basetest
from skg.doi import DOI
from skg.dblp import Dblp
from dataclasses import dataclass
from unittest import IsolatedAsyncioTestCase
import json

@dataclass
class DOIExample:
    doi: str
    isDoi: bool
    
class TestDOI(Basetest):
    """
    test DOI access
    """
    
    def testDOICheck(self):
        """
        check DOI regex
        """
        doi_examples=[
            DOIExample("10.1007/11581116_19",True),
            DOIExample("10.1109/TBDATA.2022.3224749",True),
            DOIExample("xyz",False)]
        for doi_example in doi_examples:
            self.assertTrue(DOI.isDOI(doi_example.doi)==doi_example.isDoi,doi_example.doi)
            
    def test_dblp_dois(self):
        """
        test dblp dois
        """
        dblp=Dblp()
        limit=5
        debug=True
        paper_records=dblp.get_paper_records("CEUR Workshop Proceedings","publishedin",limit=limit,debug=debug)
        for paper_record in paper_records:
            print(paper_record)
           
class TestDOILookup(IsolatedAsyncioTestCase): 
    """
    test DOI lookup
    """
    async def testDOILookup(self):
        """
        test DOI lookup 
        """
        debug=True
        dois=["10.1109/TBDATA.2022.3224749"]
        expected=["@article{Li_2022,","@inproceedings{Faruqui_2015,"]
        for i,doi in enumerate(dois):
            doi_obj=DOI(doi)
            result=await doi_obj.doi2bibTex()
            if debug:
                print(result)
            self.assertTrue(result.startswith(expected[i]))
            
    async def testCiteproc(self):
        """
        cite proc lookup
        """ 
        dois=["10.3115/v1/N15-1184","10.1007/s13042-022-01686-5","10.3390/info13120562"]
        debug=True
        for doi in dois:
            doi_obj=DOI(doi)
            json_data=await doi_obj.doi2Citeproc()
            if debug:
                print(json.dumps(json_data,indent=2))
            self.assertTrue("DOI" in json_data)
            self.assertEqual(doi.lower(),json_data["DOI"])
        
    async def testDataCiteLookup(self):
        """
        test the dataCite Lookup api
        """
        debug=True
        dois=["10.5438/0012"]
        for doi in dois:
            doi_obj=DOI(doi)
            json_data=await doi_obj.dataCiteLookup()
            if debug:
                print(json.dumps(json_data,indent=2))
            self.assertTrue("data" in json_data)
            data=json_data["data"]
            self.assertTrue("id" in data)
            self.assertEquals(doi,data["id"])
            pass
                            
   