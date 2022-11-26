'''
Created on 2022-11-22

@author: wf
'''
from tests.basetest import Basetest
from skg.doi import DOI
from skg.dblp import Dblp

class TestDOI(Basetest):
    """
    test DOI access
    """
    
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