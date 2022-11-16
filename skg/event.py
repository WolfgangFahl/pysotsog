'''
Created on 2022-11-16

@author: wf
'''
import skg.graph

class Event(skg.graph.Node):
    """
    an instance of a scientific event
    """
    
    @classmethod
    def getSamples(cls):
        samples=[
            {
                "wikiDataId":"Q112055391",
                "title": "The Third Wikidata Workshop",
                "location": "Hangzhou",
                "point_in_time": "2022-10-24",
                "official_website": "https://wikidataworkshop.github.io/2022/"
            }
        ]
        return samples
                
