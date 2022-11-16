'''
Created on 2022-11-16

@author: wf
'''
from tests.basetest import Basetest
from skg.sotsog import SotSog
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
                "search": ["Wikidata Workshop 2022"],
            }, 
            {
                "search": ["Albert","Einstein"],
            },
            {
                "search": ["Designing the web for an open society"]
            },
        ]
        for _i,search_example in enumerate(search_examples):
            search=search_example["search"]
            items=sotsog.search(search,show=False, open_browser=False)        
            for item in items:
                print(item)
