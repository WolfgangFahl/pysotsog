'''
Created on 2022-11-21

@author: wf
'''
from tests.base_skg_test import BaseSkgTest
from skg.graph import Node
from skg.location import Country

class TestLocation(BaseSkgTest):
    """
    test concerning the scholar/author concept
    """
    
    def test_locations_by_wikidata_id(self):
        """
        test searching locations 
        """
        country_concept=self.skg_def.concepts["Country"]
        id_examples=[
            {
                "id_name": "iso_code",
                "id_value": "SG",
                "concept": country_concept,
                "example": Country.getSamples()[0]
            },
        ]
        
        def checkItem(item:Node,id_name:str,id_value:str,debug:bool=False):
            """
            check the given item
            
            Args:
                item(Node): the item to check
                id_name(str): the name of the id used to retrieve the item
                id_value(str) the value that has been used to retriebe the item
                debug(bool): if True show debug information
            """
            # @TODO check against id_example
            self.assertEqual("SG",item.iso_code)
            self.assertEqual(5866139.0,item.population)
            self.assertTrue("Q334" in item.wikiDataId)
            pass
            
            
        debug=self.debug
        debug=True
        self.check_id_examples(id_examples, createFunc=Node.from_wikidata_via_id,checkItem=checkItem,debug=debug)            
