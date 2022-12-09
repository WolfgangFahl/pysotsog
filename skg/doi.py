'''
Created on 2022-11-22

@author: wf
'''
import re
import aiohttp

class DOI:
    """
    Digital Object Identifier handling
    
    see e.g. https://www.wikidata.org/wiki/Property:P356
    see https://www.doi.org/doi_handbook/2_Numbering.html#2.2
    
    """
    pattern=re.compile(r"((?P<directory_indicator>10)\.(?P<registrant_code>[0-9]{4,})(?:\.[0-9]+)*(?:\/|%2F)(?:(?![\"&\'])\S)+)")
  
    def __init__(self,doi:str):
        """
        a DOI
        """
        self.doi=doi
        match=re.match(DOI.pattern,doi)
        self.ok=bool(match)
        if self.ok:
            self.registrant_code=match.group("registrant_code")
        
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
        doi_obj=DOI(doi)
        return doi_obj.ok
    
    async def fetch_text(self,url,headers):
        """
        fetch text for the given url with the given headers
        """
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as response:
                return await response.text()
    
    async def doi2bibTex(self):
        """
        get the bibtex result for my doi
        """
        url=f"https://doi.org/{self.doi}"
        headers= {
            'Accept': 'application/x-bibtex; charset=utf-8'
        }
        return await self.fetch_text(url,headers)                 
                    
       