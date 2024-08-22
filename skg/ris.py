"""
Created on 2024-03-08

@author: wf
"""

from dataclasses import field
from typing import List, Optional

import rispy
from ez_wikidata.wdproperty import PropertyMapping, WdDatatype
from lodstorage.yamlable import lod_storable


@lod_storable
class RIS_Entry:
    """
    Research Information Systems format
    https://en.wikipedia.org/wiki/RIS_(file_format)
    """

    type_of_reference: Optional[str] = None
    abstract: Optional[str] = None
    type_of_work: Optional[str] = None
    year: Optional[str] = None
    doi: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    first_authors: List[str] = field(default_factory=list)
    publisher: Optional[str] = None
    language: Optional[str] = None
    primary_title: Optional[str] = None
    urls: List[str] = field(default_factory=list)
    secondary_title: Optional[str] = None

    @property
    def lang_qid(self) -> str:
        qid = "Q1860"  # English
        if self.language == "de":
            qid = "Q188"
        return qid

    @classmethod
    def get_property_mappings(cls):
        """
        get the wikidata property mappings
        """
        mappings = [
            PropertyMapping(
                column="instanceof",
                propertyName="instanceof",
                propertyId="P31",
                propertyType=WdDatatype.itemid,
                value="Q13442814",  # scholarly article
            ),
            PropertyMapping(
                column="primary_title",
                propertyName="title",
                propertyId="P1476",
                propertyType=WdDatatype.text,
            ),
            PropertyMapping(
                column="doi",
                # propertyName="DOI",
                # propertyId="P356",
                propertyName="described at URL",
                propertyId="P973",
                # propertyType=WdDatatype.extid,
                propertyType=WdDatatype.url,
            ),
            PropertyMapping(
                column="lang_qid",
                propertyName="language of work or name",
                propertyId="P407",
                propertyType=WdDatatype.itemid,
            ),
            PropertyMapping(
                column="year",
                propertyName="publication date",
                propertyId="P577",
                propertyType=WdDatatype.year,
            ),
        ]
        return mappings

    @classmethod
    def get_dict_from_file(cls, ris_file_path, by_field: str = "index"):
        ris_dict = {}
        with open(ris_file_path, "r") as bibliography_file:
            entries = rispy.load(bibliography_file)
            for i, entry in enumerate(entries, start=1):
                ris_entry = RIS_Entry.from_dict(entry)
                if by_field == "index":
                    value = i
                else:
                    if by_field in entry:
                        value = field[entry]
                ris_dict[value] = ris_entry

        return ris_dict
