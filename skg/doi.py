'''
Created on 2022-11-22

@author: wf
'''
import re
class DOI:
    """
    Digital Object Identifier handling
    
    see e.g. https://www.wikidata.org/wiki/Property:P356
    """
    pattern=re.compile(r"(10\.[0-9]{4,}(?:\.[0-9]+)*(?:\/|%2F)(?:(?![\"&\'])\S)+)")
  
    def __init__(self):
        """
        a DOI
        """
        
    @classmethod
    def isDOI(cls,doi:str):
        """
        check that the given string is a doi
        
        Args:
            doi(str): the potential DOI string
        """
        if not doi:
            return False
        if isinstance(doi,list):
            ok=len(doi)>0
            for single_doi in doi:
                ok=ok and cls.isDOI(single_doi)
            return ok
        if not isinstance(doi,str):
            return False
        match=re.match(cls.pattern,doi)
        return bool(match)