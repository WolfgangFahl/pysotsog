'''
Created on 2022-11-21

@author: wf
'''
import skg.graph

class Country(skg.graph.Node):
    """
    an instance of a country
    """
    
    @classmethod
    def getSamples(cls):
        samples=[
            {
                "wikiDataId":"Q334",
                "name": "Singapore",
                "iso_code": "SG", 
                "homepage": "https://www.gov.sg/",
                "population": 5866139,
                "coordinate_location": "1°18'N, 103°48'E"
            }
        ]
        return samples
