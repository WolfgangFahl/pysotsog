'''
Created on 2022-11-16

@author: wf
'''
from tests.basetest import Basetest
from skg.sotsog import SotSog
from skg.search import SearchOptions
class TestSotsog(Basetest):
    """
    test concerning the SotSog main class
    """

    def test_sotsog_search(self):
        """
        test searches
        """
        sotsog=SotSog()
        search_examples=[
            {
                "search": ["10.1145/1963405.1963408"],
                "qid": "Q55693406", 
                "concept": "Paper"
            },
            {
                "search": ["RWTH"],
                "qid": "Q273263",
                "concept": "Institution"
            }, 
            {
                "search": ["Wikidata Workshop 2022"],
                "qid": "Q112055391", 
                "concept": "Event"
            }, 
            {
                "search": ["VNC"],
                "qid": "Q105695678", 
                "concept": "EventSeries"
            }, 
            {
                "search": ["Albert","Einstein"],
                "qid": "Q937",
                "concept":  "Scholar"
            },
            {
                "search": ["Designing the web for an open society"],
                "qid": "Q55693406", 
                "concept": "Paper"
            },
        ]
        debug=self.debug
        debug=True
        for _i,search_example in enumerate(search_examples):
            search=search_example["search"]
            qid=search_example["qid"]
            concept_name=search_example["concept"]
            options=SearchOptions(show=False, open_browser=False)
            s_result=sotsog.search(search,options)        
            for item in s_result.items:
                if debug:
                    print(item)
            for item in s_result.items:
                self.assertEqual(concept_name,item.concept.name)
                if hasattr("item", "wikiDataId"):
                    self.assertTrue(qid in item.wikiDataId)
                # @TODO compare properties against samples
                
    def test_get_markups(self):
        """
        get markups for a given DOI
        """
        sotsog=SotSog()
        options=SearchOptions(show=False, open_browser=False)
        dois=["10.7287/peerj.preprints.27466v1"]
        #@TODO test search via DOI, ORCID and so on
