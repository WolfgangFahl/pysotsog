'''
Created on 17.11.2022

@author: wf
'''
import skg
import habanero
import habanero.cn as cn
from skg.citeproc import Citeproc

class Crossref:
    """
    Crossref access
    """
    
    def __init__(self,mailto=None,ua_string=None):
        """
        constructor
        """
        if mailto is None:
            mailto="wf@bitplan.com"
        if ua_string is None:
            ua_string=f"pysotsog/{skg.__version__} (https://pypi.org/project/pysotsog/; mailto:{mailto})"
        #self.cr = habanero.Crossref(mailto=mailto,ua_string=ua_string)  
        self.cr = habanero.Crossref(ua_string="")  
    
    def doiMetaData(self, dois:list):
        """ 
        get the meta data for the given dois
        
        Args:
            doi(list): a list of dois
        """
        metadata = None
        response = self.cr.works(ids=dois)
        if 'status' in response and 'message' in response and response['status'] == 'ok':
            metadata = response['message']
        return metadata
    
    def doiBibEntry(self,dois:list):
        """
        get bib entries for the given dois
        """
        bibentry=cn.content_negotiation(ids = dois, format = "bibentry")
        return bibentry
    
    def asScite(self,meta_data:dict)->str:
        """
        convert the given meta data to #Scite format
        
        see https://github.com/SemanticMediaWiki/SemanticCite/blob/master/src/FilteredMetadata/BibliographicFilteredRecord.php
        
        Returns:
            str: Semantic Mediawiki markup
        """
        markup=Citeproc.asScite(meta_data,retrieved_from=self.cr.base_url)
        return markup
        