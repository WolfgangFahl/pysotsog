'''
Created on 2022-11-16

@author: wf
'''
from skg.scholar import Scholar,Institution
from skg.paper import Paper
from skg.event import Event,EventSeries,Proceedings
from skg.graph import Concept


class SKG_Def:
    """
    scholary knowledge graph
    """
    
    def __init__(self):
        """
        constructor
        """
        self.concepts={
            "Scholar": Concept(name="Scholar",cls=Scholar),
            "Institution": Concept(name="Institution",cls=Institution),
            "Paper": Concept(name="Paper",cls=Paper),
            "Event": Concept(name="Event",cls=Event),
            "EventSeries": Concept(name="EventSeries",cls=EventSeries),
            "Proceedings": Concept(name="Proceedings",cls=Proceedings)
        }
        self.concepts["Scholar"].map_wikidata("Q5","author",[
            ("name","label"),
            ("dblpId","P2456"),
            ("gndId","P227"),
            ("linkedInId","P6634"),
            ("homepage","P856"),
            ("googleScholarUser","P1960"),("orcid","P496"),
            ("givenName","P735"),
            ("familyName","P734"),
            ("gender","P21"),
            ("image","P18"),
            ("occupation","P106")
        ])
        self.concepts["Institution"].map_wikidata("Q4671277","organization",[
            ("short_name","P1813"), # 2.0 % 
            ("inception","P571"), # 65.8 %
            ("image","P18"), # 15.2 % 
            ("country","P17"), # 88.8 %
            ("located_in","P131"), # 51.9 %
            ("official_website","P856"), # 59.1%
            ("coordinate_location","P625") # 44.0 %
        ])  
        self.concepts["Paper"].map_wikidata("Q13442814","work",[
            ("title","label"),
            ("DOI","P356"),
            ("DBLP_publication_ID","P8978"),
            ("publication_date","P577")
        ])
        # scientific event
        self.concepts["Event"].map_wikidata("Q52260246","event",[
            ("title","P1476"),
            ("location","P276"),
            ("point_in_time","P585"),
            ("official_website","P856")
        ])
        # academic event series
        self.concepts["EventSeries"].map_wikidata("Q47258130","event-series",[
            ("title","P1476"), # 96.7 %
            ("short_name","P1813"), # 93.1 %
            ("VIAF_ID","P214"), # 60.5 %
            ("DBLP_venue_ID","P8926"), # 96.4 %
            ("gndId","P227"), #42.3 %
            ("inception","P571"), # 22.3 %
            ("official_website","P856") # 13.5 %
        ])
        # proceedings
        self.concepts["Proceedings"].map_wikidata("Q1143604","venue",[
            ("title","P1476"),
            ("short_name","P1813"),
            ("full_work_available_at_URL","P953"),
            ("publication_date","P577")
        ])
                      
        self.concepts_by_qid={}
        for concept in self.concepts.values():
            if concept.wd_class in self.concepts_by_qid:
                raise Exception(f"duplicate wd_class definition: {concept.wd_class}")
            self.concepts_by_qid[concept.wd_class]=concept
        
    def conceptForQid(self,qid:str)->Concept:
        """
        get the concept for the given wikidata Q Identifieer
        
        Args:
            qid(str): get the concept for the given Qid
            
        Return:
            Concept: or None if none is found
        """
        concept=self.concepts_by_qid.get(qid,None)
        return concept
        