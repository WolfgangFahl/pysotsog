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
            {
                "wikiDataId":"Q54303353",
                "name": "Stefan Decker",
                "gndId":"",
                "dblpId":"d/StefanDecker",
                "orcid":"0000-0001-6324-7164",
                "linkedInId":"",
                "googleScholarUser":"uhVkSswAAAAJ",
                "homepage":"http://www.stefandecker.org"
            },
            {
                "name": "Tim Berners-Lee",
                "wikiDataId": "Q80",
                "givenName": "Timothy",
                "familyName": "Berners-Lee" 
            }
        ]
        return samples
        
    
    def __init__(self):
        """
        constructor
        """