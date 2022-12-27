'''
Created on 2022-11-16

@author: wf
'''
from skg.scholar import Scholar,Institution
from skg.paper import Paper
from skg.event import Event,EventSeries,Proceedings
from skg.location import Country
from skg.graph import Concept
import datetime
from skg.version import Version

class SKG_Def:
    """
    scholary knowledge graph
    """
    
    def __init__(self):
        """
        constructor
        """
        self.concepts={
            # main concepts
            "Scholar": Concept(name="Scholar",cls=Scholar),
            "Institution": Concept(name="Institution",cls=Institution),
            "Paper": Concept(name="Paper",cls=Paper),
            "Event": Concept(name="Event",cls=Event),
            "EventSeries": Concept(name="EventSeries",cls=EventSeries),
            "Proceedings": Concept(name="Proceedings",cls=Proceedings),
            # neighbour concepts
            "Country": Concept(name="Country",cls=Country)
        }
        self.concepts["Scholar"].map_wikidata("Q5","author",[
            ("name","label"),
            ("dblpId","P2456"),
            ("gndId","P227"),
            ("linkedInId","P6634"),
            ("homepage","P856"),
            ("googleScholarUser","P1960"),
            ("orcid","P496"),
            ("givenName","P735"),
            ("familyName","P734"),
            ("gender","P21"),
            ("image","P18"),
            ("occupation","P106"),
            ("Semantic_Scholar_author_ID","P4012")
        ]).map("dblp",[
            ("name","primaryCreatorName"),
            ("homepage","primaryHomepage"),
            ("orcid","orcid")
        ]).map("smw",[
            ("wikiDataId","wikiDataId"),
            ("familyName","name"),
            ("givenName","firstName"),
            ("googleScholarUser","googleScholarUser"),
            ("homepage","homepage"),
            ("dblpId","dblpId"),
            ("orcid","orcid"),
            ("linkedInId","linkedInId")
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
            ("doi","P356"),
            ("DBLP_publication_ID","P8978"),
            ("publication_date","P577")
        ]).map("dblp",[
            ("title","title"),
            ("doi","doi")
        ])
        # scientific event
        self.concepts["Event"].map_wikidata("Q52260246","event",[
            ("title","P1476"),
            ("country","P17"), # 93.9% -> Human Settlement
            ("location","P276"), # 94.6%
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
        # country
        self.concepts["Country"].map_wikidata("Q6256","topic",[
            ("name","label"), # 100% ?
            ("homepage","P856"), # 49.4%
            ("population","P1082"), # 57.4%
            ("capital","P36"), #59.8%
            ("coordinate_location","P625"), #58.6%
            ("iso_code","P297") # 53.3%
            
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
    
    def toPlantuml(self,header:str=None, footer:str=None)->str:
        """
        get a plantuml version of this knowledge graph
        
        Args:
            header(str): the header to apply
            footer(str): the footer to apply
        
        Returns:
            str: the plantuml markup
    
        """
        timestamp=datetime.datetime.utcnow().strftime('%Y-%m-%d')
        if header is None:
            header=f"""/'{Version.name}:{Version.description}
updated {timestamp}
      
authors:{Version.authors} 
'/
title  {Version.name}:{Version.description} see {Version.doc_url} updated {timestamp}
hide circle
package skg {{
"""
        if footer is None:
            footer="}\n"
        markup=f"{header}"
        indent="  "
        for concept_name,concept in self.concepts.items():
            markup+=f"""{indent}class {concept_name} {{\n"""
            for prop_name,prop in concept.props.items():
                markup+=f"""{indent}  {prop_name}\n"""
            markup+=f"""\n{indent}}}\n"""
        markup+=f"{footer}"
        return markup
    
    def toSiDiF(self)->str:
        """
        convert me to SiDiF format
        """
        sidif=""
        for concept_name,concept in self.concepts.items():
            sidif+=f"""#
# {concept_name}
#
{concept_name} isA Topic
"{concept_name} is name of it
"""
        return sidif
        