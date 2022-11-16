'''
Created on 2022-11-16

@author: wf
'''
from skg.scholar import Scholar
from skg.paper import Paper
from skg.event import Event
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
            "Paper": Concept(name="Paper",cls=Paper),
            "Event": Concept(name="Event",cls=Event)
        }
        self.concepts["Scholar"].map_wikidata("Q5","author",[
            ("name","label"),
            ("dblpId","P2456"),("gndId","P227"),
            ("linkedInId","P6634"),
            ("homepage","P856"),
            ("googleScholarUser","P1960"),("orcid","P496"),
            ("givenName","P735"),
            ("familyName","P734")
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
        