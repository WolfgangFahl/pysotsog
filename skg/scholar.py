'''
Created on 2022-11-16

@author: wf
'''
import skg.graph


class Scholar(skg.graph.Node):
    """
    an instance of a scholar that writes papers to be an author
    """
    
    @classmethod
    def getSamples(cls):
        samples=[
            {"wikiDataId":"Q54303353",
             "gndId":"",
             "dblpId":"d/StefanDecker",
             "orcid":"0000-0001-6324-7164",
             "linkedInId":"",
             "googleScholarUser":"uhVkSswAAAAJ",
             "homepage":"http://www.stefandecker.org"
             }]
        return samples
        
    
    def __init__(self):
        """
        constructor
        """
        
    def scholia_url(self):
        """
        get my scholia url
        """
        prefix="https://scholia.toolforge.org/author"
        wd_url=getattr(self, "wikiDataId",None)
        if wd_url is None:
            return prefix
        else:
            qid=wd_url.replace("http://www.wikidata.org/entity/","")
            return f"{prefix}/{qid}"