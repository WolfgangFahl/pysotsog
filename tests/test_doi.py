'''
Created on 2022-11-22

@author: wf
'''
from tests.basetest import Basetest
from skg.doi import DOI
from skg.dblp import Dblp
from dataclasses import dataclass

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
        doi_examples=[DOIExample("10.1007/11581116_19",True),DOIExample("xyz",False)]
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