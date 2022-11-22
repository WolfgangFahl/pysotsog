'''
Created on 2022-11-16

@author: wf
'''
from tests.base_skg_test import BaseSkgTest
from skg.scholar import Scholar
from skg.graph import Node
from skg.smw import SemWiki

class TestScholar(BaseSkgTest):
    """
    test concerning the scholar/author concept
    """
    
    def test_scholar_by_wikidata_id(self):
        """
        test searching a scholar/author by ORCID,dblpId or wikiDataId from
        wikidata
        """
        author_concept=self.skg_def.concepts["Scholar"]
        id_examples=[
            {
                "id_name": "orcid",
                "id_value": "0000-0003-1279-3709",
                "concept": author_concept
            },
            {
                "id_name": "dblpId",
                "id_value": "b/TimBernersLee",
                "concept": author_concept
            },
            {
                "id_name": "wikiDataId",
                "id_value": "Q80",
                "concept": author_concept
            },           
        ]
        
        def checkItem(scholar:Scholar,id_name:str,id_value:str,debug:bool=False):
            """
            check the given item
            
            Args:
                item(Node): the item to check
                id_name(str): the name of the id used to retrieve the item
                id_value(str) the value that has been used to retriebe the item
                debug(bool): if True show debug information
            """
            self.assertEqual("Tim Berners-Lee",scholar.label)
            self.assertEqual("https://scholia.toolforge.org/author/Q80",scholar.scholia_url())
            
        debug=self.debug
        debug=True
        self.check_id_examples(id_examples, createFunc=Node.from_wikidata_via_id,checkItem=checkItem,debug=debug)            

    def test_smw_markup(self):
        """
        test Semantic MediaWiki markup for a scholar
        """
        orcids=["0000-0002-4030-0978"]
        author_concept=self.skg_def.concepts["Scholar"]
        for orcid in orcids:
            scholars=Node.from_wikidata_via_id(author_concept, "orcid", orcid)
            scholar=scholars[0]
            markup=SemWiki.asMarkup(scholar)
            print (markup)
            