'''
Created on 22.11.2022

@author: wf
'''
from wikibot.smw import SMW
from wikibot.wikiuser import WikiUser
from wikibot.wikiclient import WikiClient
from wikibot.smw import SMWClient

class SemWiki:
    """
    access to Semantic mediawiki
    """
    
    def __init__(self,wikiUser:WikiUser,withLogin:bool=False):
        """
        
        constructor
        
        Args:
            wikiUser:WikiUser
        """
        self.wikiUser=wikiUser
        self.wikiClient=WikiClient.ofWikiId(wikiUser.wikiId)
        if withLogin:
            self.wikiClient.login()
        self.smw=SMWClient(self.wikiClient.getSite())
    
        
    def id_refs(self,mainlabel="pageTitle",condition="DOI::+",title:str="DOI references",askExtra:str="",id_prop="DOI",id_name="doi")->list:
        """
        get a list of DOI references from the given wiki
        """
        ask = f"""{{{{#ask:[[{condition}]]{askExtra}
|?{id_prop}={id_name}
|mainlabel={mainlabel}
|?Creation_date=creationDate
|?Modification_date=modificationDate
|?Last_editor_is=lastEditor
}}}}
"""
        refs=self.smw.query(ask,title)
        return refs
            
    def papers(self):
        """
        get the paper records
        """
        askExtra="""\n|?Citation_text=reference"""
        paper_records=self.id_refs(condition="Citation_text::+",title="doi paper referencs", askExtra=askExtra)
        return paper_records
    
    def scholars(self):
        """
        get scholars
        """
        condition="Concept:Scholar"
        mainlabel="Scholar"
        askExtra="""
| ?Scholar name = name
| ?Scholar firstName = firstName
| ?Scholar homepage = homepage
| ?Scholar orcid = orcid
| ?Scholar dblpId = dblpId
| ?Scholar googleScholarUser = googleScholarUser
| ?Scholar linkedInId = linkedInId
| ?Scholar gndId = gndId
| ?Scholar smartCRMId = smartCRMId
|sort=Scholar name,Scholar firstName
|order=ascending,ascending
"""       
        scholars=self.id_refs(mainlabel, condition, "scholars", askExtra, "Scholar wikiDataId", "wikiDataId")
        return scholars
        