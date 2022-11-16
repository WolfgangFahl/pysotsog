'''
Created on 2022-11-16

@author: wf
'''
from skg.scholar import Scholar
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
            "Scholar": Concept(name="Scholar",samples=Scholar.getSamples())
        }
        self.concepts["Scholar"].map_wikidata("Q5",[
            ("dblpId","P2456"),("gndId","P227"),
            ("linkedInId","P6634"),
            ("homepage","P6634"),
            ("googleScholarUser","P1960"),("orcid","P496")])