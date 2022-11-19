'''
Created on 2022-11-16

@author: wf
'''
import skg.graph

class Paper(skg.graph.Node):
    '''
    a scientific paper
    '''

    @classmethod
    def getSamples(cls):
        samples=[
            { 
                "wikiDataId": "Q55693406",
                "title":"Designing the web for an open society",
                "doi": "10.1145/1963405.1963408",
                "DBLP_publication_ID": "conf/www/Berners-Lee11", 
                "publication_date": 2011,
            },
            {
                "doi": "10.1007/978-3-031-19433-7_21",
                "title": "An Analysis of Content Gaps Versus User Needs in the Wikidata Knowledge Graph"
            }
        ]
        return samples
        
    def __init__(self):
        '''
        Constructor
        '''
        