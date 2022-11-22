'''
Created on 2022-11-22

@author: wf
'''
# see https://pypi.org/project/semanticscholar/
from semanticscholar import SemanticScholar as SemScholar

class SemanticScholar:
    """
    wrapper for Semantic Scholar API
    """
    
    def __init__(self):
        """
        constructor
        """
        self.sch = SemScholar()
        
    def get_paper(self,doi:str):
        """
        get the paper with the given DOI identifier
        """
        paper=self.sch.get_paper(doi)
        return paper
    
    def get_author(self):
        """
        https://api.semanticscholar.org/api-docs/graph#tag/Author-Data/operation/get_graph_get_author_search
        """
        pass
        