'''
Created on 2022-11-19

@author: wf
'''

class SearchOptions:
    """
    wrapper for search results
    """
    def __init__(self,limit:int=9,lang='en',show:bool=True,
               bibtex:bool=False,scite:bool=False,open_browser:bool=False):
        """
        constructor
        
        Args:
            limit(int): limit for the maximum number of results
            lang(str): the language code to use for the search
            show(bool): if True print the search results
            bibtex(bool): if True output bibtex for fitting search results
            scite(bool): if True output #scite SMW Semantic Cite format
            open_browser(bool): if True open a browser for the target page of the item e.g. scholia

        """
        self.limit=limit
        self.lang=lang
        self.show=show
        self.bibtex=bibtex
        self.scite=scite
        self.open_browser=open_browser
        
class SearchResult:
    """
    wrapper for search results
    """
    def __init__(self,search_list:list,options=SearchOptions):
        """
        constructor
        
         Args:
            search_list(list): a list of search terms
            options(SearchOptions): the search options to apply
        """
        self.search_list=search_list
        self.options=options