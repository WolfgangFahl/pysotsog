"""
Created on 2024-03-08

@author: wf
"""
import json
import re
from ngwidgets.basetest import Basetest
from skg.ris import RIS_Entry
import os
from pathlib import Path
from ez_wikidata.wdsearch import WikidataSearch
from ez_wikidata.wikidata import Wikidata
from ez_wikidata.wdproperty import PropertyMapping, WdDatatype
from lodstorage.sparql import SPARQL
from lodstorage.query import QueryManager

class STT_Paper:
    """
    Softwaretechnik Trend Paper
    """
    def __init__(self,ris_entry:RIS_Entry):
        self.paper=ris_entry
        regex = r"Band (\d+), Heft (\d+)"
        match = re.search(regex, self.paper.secondary_title)
        self.property_mappings=RIS_Entry.get_property_mappings()
        self.property_mappings.extend([ 
            PropertyMapping(
                    column="published in",
                    propertyName="published in",
                    propertyId="P1433",
                    propertyType=WdDatatype.itemid,
                    value="Q96731774", # Softwaretechnik-Trends
            ),
            PropertyMapping(
                    column="volume",
                    propertyName="volume",
                    propertyId="P478",
                    propertyType=WdDatatype.string,
            ),
            PropertyMapping(
                    column="issue",
                    propertyName="issue",
                    propertyId="P433",
                    propertyType=WdDatatype.string,
            )
        ]
        )
        record=self.paper.to_dict()
        record["lang_qid"]=self.paper.lang_qid
        record["label"]=self.paper.primary_title
        record["description"]="Paper in Software Technik Trends"
        record["volume"] = match.group(1)
        record["issue"] = match.group(2)
        self.record=record
        
        
class TestRis2Wikidata(Basetest):
    """
    Test RIS to wikidata conversion
    
    see https://www.wikidata.org/wiki/Q116769124 as an example paper
    """
    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        # Define the folder and file name
        folder = "/Projekte/2024/Promotion/STT"
        file_name = "metadata-exporthttps --dl.gi.de-handle-20.500.12116-4669.ris"
        home_directory = str(Path.home())     
        self.ris_file_path = os.path.join(home_directory, folder.strip("/"), file_name)
        self.ris_dict=None
        if os.path.exists(self.ris_file_path):
            self.ris_dict=RIS_Entry.get_dict_from_file(self.ris_file_path)
        
    def test_dblp_stt(self):
        """
        test Softwaretechnik Trend entries in dblp
        """
        endpoint="https://qlever.cs.uni-freiburg.de/api/dblp/query"
        sparql = SPARQL(endpoint)
        path = os.path.dirname(__file__)
        qYamlFile = f"{path}/../skg/resources/queries/stt.yaml"
        if os.path.isfile(qYamlFile):
            qm = QueryManager(lang="sparql", queriesPath=qYamlFile)
        query = qm.queriesByName["STT-Papers"]
        lod = sparql.queryAsListOfDicts(query.query)
        debug=True
        if debug:
            print(f"found {len(lod)} STT papers")
    
        
    def testPaper(self):
        """
        test adding a single paper to Wikidata
        """
        # ParTeG - A Model-Based Testing Tool
        wd=Wikidata()
        wd.loginWithCredentials()
        paper=STT_Paper(self.ris_dict[416])
        print(json.dumps(paper.record,indent=2,default=str))
        #return
        write=True
        result=wd.add_record(
            paper.record, 
            property_mappings=paper.property_mappings,
            item_id="Q124789410",
            lang="en", 
            write=write,
            ignore_errors=False, 
            summary="bot style created entry")
        print(result.pretty_item_json)
        print(result.errors)
        print(result.msg)
        print(result.qid)
        
    def testSTT(self):
        """
        test importing Software Technik Trends papers
        """
        # Check if the file exists and read it if it does
        if not self.ris_dict:
            return
        wd_search=WikidataSearch()
        debug=self.debug
        debug=True

        if debug:
            print(f"found {len(self.ris_dict)} RIS entries")
            start=400
            end=600
            for i in range(start,end):
                ris_entry=self.ris_dict[i]
                hits=wd_search.search(ris_entry.primary_title)
                print(f"{i:2}:{ris_entry.primary_title}")
                for hit in hits:
                    print(hit)
 

