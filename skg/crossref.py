'''
Created on 17.11.2022

@author: wf
'''
import skg
import habanero
import habanero.cn as cn

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
        self.cr = habanero.Crossref(mailto=mailto,ua_string=ua_string)  
    
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
    
    def doiBibEntry(self,doi:str):
        bibentry=cn.content_negotiation(ids = doi, format = "bibentry")
        return bibentry
        