'''
Created on 2022-11-16

@author: wf
'''
from tests.basetest import Basetest
from skg.scholar import Scholar
from skg.kg import SKG_Def

class TestScholar(Basetest):
    """
    test concerning the scholar/author concept
    """
    
    def test_scholar_by_id(self):
        """
        test searching a scholar/author by ORCID
        """
        id_examples=[
            {
                "id_name": "orcid",
                "id_value": "0000-0003-1279-3709"
            },
            {
                "id_name": "dblpId",
                "id_value": "b/TimBernersLee"
            },
            {
                "id_name": "wikiDataId",
                "id_value": "Q80"
            },           
        ]
        debug=self.debug
        debug=True
        skg_def=SKG_Def()
        for id_example in id_examples:
            id_name=id_example["id_name"]
            id_value=id_example["id_value"]
            scholars=Scholar.from_wikidata_via_id(skg_def.concepts["Scholar"],id_name,id_value)
            if debug:
                for scholar in scholars:
                    print(scholar)
            self.assertEqual(1,len(scholars))
            scholar=scholars[0]
            self.assertEqual("Tim Berners-Lee",scholar.label)
            self.assertEqual("https://scholia.toolforge.org/author/Q80",scholar.scholia_url())
