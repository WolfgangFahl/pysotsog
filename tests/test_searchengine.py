'''
Created on 2022-18-11

@author: wf
'''
from tests.basetest import Basetest
from skg.searchengine import InternetSearch
import pprint

class TestSearchEngine(Basetest):
    """
    test search engine
    """
    
    def test_searchengines(self):
        """
        test search engines
        """
        i_search=InternetSearch()
        search_terms=["LinkClus: efficient clustering via heterogeneous semantic links"]
        for search_term in search_terms:
            for engine_name,results in i_search.search(search_term):
                print (engine_name)
                pprint.pprint(results)
        
