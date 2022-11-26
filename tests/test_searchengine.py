'''
Created on 2022-18-11

@author: wf
'''
from tests.basetest import Basetest
from skg.searchengine import InternetSearch
from skg.dblp import Dblp
import pprint
from collections import Counter

class TestSearchEngine(Basetest):
    """
    test search engine
    """
    
    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.counters={
            "sites": Counter(),
            "types": Counter(),
        }
    
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
                
    def analyse_isearch_result(self,results):
        """
        analyse the given search engine results
        """
        for record in results:
            titles=record["titles"]
            parts=titles.split("›")
            site=parts[0]
            self.counters["sites"][site]+=1
            if len(parts)>1:
                rtype=parts[1]
                self.counters["types"][rtype]+=1
            pass
        pass
    
    def check_search(self,search_term:str):
        i_search=InternetSearch()
        for engine_name,results in i_search.search(search_term):
            print (engine_name)
            self.analyse_isearch_result(results)
            pprint.pprint(results)
        for name,counter in self.counters.items():
            print(name)
            print(counter.most_common(10))
        
    def test_dblp_titles(self):
        """
        test DBLP titles
        """
        dblp=Dblp()
        limit=5
        paper_records=dblp.get_paper_records("ARCS","publishedin",limit=limit)
        for paper_record in paper_records:
            print(paper_record)
            title=paper_record["title"]
            self.check_search(title)
            
    def test_google_scholar(self):
        """
        """
        scholars=["Suchetha N. Kunnath"]
        for scholar in scholars:
            self.check_search(scholar)
        
            
    def test_paper_search(self):
        """
        test the search for papers
        """
        titles=["Constance: an intelligent data lake system"]
        for title in titles:
            self.check_search(title)
        
        
            
