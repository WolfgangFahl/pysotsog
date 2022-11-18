'''
Created on 2022-11-17

@author: wf
'''
from tests.basetest import Basetest
from skg.dblp import Dblp

class TestDblp(Basetest):
    """
    test dblp access
    """
    
    def test_dblp(self):
        """
        test dblp access
        """
        
    def test_dblp_schema(self):
        """
        test loading the dblp schema
        """
        dblp=Dblp()
        dblp.loadSchema()
        