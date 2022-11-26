'''
Created on 18.11.2022

@author: wf
'''
from search_engine_parser.core.engines.bing import Search as BingSearch
from search_engine_parser.core.engines.google import Search as GoogleSearch
from search_engine_parser.core.engines.yahoo import Search as YahooSearch
from search_engine_parser.core.engines.duckduckgo import Search as DuckDuckGoSearch
from search_engine_parser.core.engines.googlescholar import Search as GoogleScholarSearch
import sys 
  
class InternetSearch:
    """
    generic internet search
    """
    
    def __init__(self,debug:bool=False):
        """
        constructor
        """
        self.debug=debug
        self.gsearch = GoogleSearch()
        self.ysearch = YahooSearch()
        self.bsearch = BingSearch()
        self.dsearch = DuckDuckGoSearch()
        self.gs_search=GoogleScholarSearch()
        self.engines=[self.gs_search,self.ysearch,self.dsearch,self.bsearch]
        
    def handleException(self,ex):
        """
        handle the given exception
        """
        if self.debug:
            print(f"{str(ex)}",file=sys.stderr)
        
    def search(self,search_term:str):
        """
        search my engines for the given search_term
        """
        search_args=(search_term, 1)
        for engine in self.engines:
            try:
                result=engine.search(*search_args)
                yield engine.name,result.results
                pass
            except Exception as ex:
                self.handleException(ex)
                pass
            
    