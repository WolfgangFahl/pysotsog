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
                "familyName": "Berners-Lee",
                "gender": "male",
                "image": "https://commons.wikimedia.org/wiki/File:Sir_Tim_Berners-Lee_(cropped).jpg",
                # "occupation": "computer scientist" truly tabular issue
            }
        ]
        return samples
        
    
    def __init__(self):
        """
        constructor
        """
        
class Institution(skg.graph.Node):
    """
    academic institution a scholar might be affiliated with
    """
    
    @classmethod
    def getSamples(cls):
        samples=[
            {
                "wikiDataId": "Q273263",
                "short_name": "RWTH Aachen (German)"
            },
            {
                "wikiDataId": "Q391028",
                "inception": "1908",
                "short_name": "UBC",
                "country": "Canada",
                "image": "https://commons.wikimedia.org/wiki/File:Irving_K._Barber_Library.jpg",
                "located_in": "Vancouver",
                "official_website": "https://www.ubc.ca/"
            }
        ]
        return samples    
    
    def __init__(self):
        """
        constructor
        """