'''
Created on 2022-12-17

@author: wf
'''
from tests.basetest import Basetest
from skg.orcid import ORCID
import json

class TestORCID(Basetest):
    """
    test ORCID handling
    """
    
    def test_orcid(self):
        """
        test ORCID access
        """
        debug=self.debug
        #debug=True
        for orcid_str in ["0000-0002-5071-1658"]:
            orcid=ORCID(orcid_str)
            self.assertTrue(orcid.ok)
            for op in ["","external-identifiers","works"]:
                md=orcid.getMetadata(op=op)
                if debug:
                    print(md)
                if op=="":
                    self.assertTrue("orcid-identifier" in md)
                elif op=="external-identifiers":
                    self.assertTrue("path" in md)
                elif op=="works":
                    if debug:
                        print(json.dumps(md["group"],indent=2))
        