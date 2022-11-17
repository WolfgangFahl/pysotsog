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
    
class EventSeries(skg.graph.Node):
    """
    an instance of an academic event series
    """
    
    @classmethod
    def getSamples(cls):
        samples=[
            {
                "wikiDataId":"Q6053150",
                "short_name":"ISWC"
            },
            {
                "wikiDataId": "Q105491257",
                "short_name": "ECDL",
                "title": "European Conference on Research and Advanced Technology for Digital Libraries (English)",
                "official_website": "http://ecdlconference.isti.cnr.it/"
            },
            {
                "wikiDataId": "Q105695678",
                "short_name": "VNC (English)",
                "DBLP_venue_ID": "conf/vnc",
                "VIAF_ID": "267408611",
                "title": "IEEE Vehicular Networking Conference"
            },
            {
                "wikiDataId":"Q17012957",
                "short_name":"ESWC",
                "inception": "2004",
                "gndId": "1091749205"
            }
        ]
        return samples
    
class Proceedings(skg.graph.Node):
    """
    Proceedings of an event
    """
    @classmethod
    def getSamples(cls):
        samples=[
            {
                "wikiDataId": "Q115053286",
                "short_name": "Wikidata 2022 (English)",
                "title": "Proceedings of the 3rd Wikidata Workshop 2022 (English)",
                "publication_date": "2022-11-03",
                "full_work_available_at_URL": "http://ceur-ws.org/Vol-3262/"
            }
        ]
        return samples
                
