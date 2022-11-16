'''
Created on 2022-11-16

@author: wf
'''
from tests.basetest import Basetest
from skg.scholar import Scholar
from skg.kg import SKG_Def

class TestScholar(Basetest):
    """
    test concerning the author concept
    """
    
    def test_scholar_by_orcid(self):
        """
        test searching a scholar/author by ORCID
        """
        orcid_examples=[
            {
                "ORCID": "0000-0003-1279-3709"
            }
        ]
        debug=self.debug
        debug=True
        skg_def=SKG_Def()
        for orcid_example in orcid_examples:
            orcid=orcid_example["ORCID"]
            scholars=Scholar.from_wikidata_via_id(skg_def.concepts["Scholar"],"orcid",orcid)
            if debug:
                for scholar in scholars:
                    print(scholar)
            self.assertEqual(1,len(scholars))
            self.assertEqual("Tim Berners-Lee",scholars[0].label)
