"""
Created on 2022-11-16

@author: wf
"""

from lodstorage.lod import LOD
from lodstorage.sparql import SPARQL


class Wikidata:
    """
    Wikidata access wrapper
    """

    instance = None

    def __init__(
        self, endpoint: str = "https://query.wikidata.org/sparql", debug: bool = False
    ):
        """
        constructor
        """
        self.endpoint = endpoint
        self.sparql = SPARQL(endpoint)
        self.debug = debug
        Wikidata.instance = self

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            Wikidata()
        return cls.instance

    @classmethod
    def getQid(self, wd_url: str):
        qid = wd_url.replace("http://www.wikidata.org/entity/", "")
        return qid

    @classmethod
    def getLabelForQid(self, qid: str, lang: str = "en") -> str:
        """
        get a label for the given Wikidata QID

        Args:
            qid(str): the Wikidata ID
            lang(str): the language
        """
        sparql_query = f"""SELECT ?itemLabel WHERE {{
  VALUES ?item {{
    wd:{qid}
  }}
  OPTIONAL {{ ?item rdfs:label ?langLabel. FILTER(LANG(?langLabel)="{lang}") }}
  OPTIONAL {{ ?item rdfs:label ?mulLabel. FILTER(LANG(?mulLabel)="mul") }}
  BIND(COALESCE(?langLabel, ?mulLabel) AS ?itemLabel)
  FILTER(BOUND(?itemLabel))
}}"""
        wd = Wikidata.getInstance()
        lod = wd.sparql.queryAsListOfDicts(sparql_query)
        label = None
        if len(lod) == 1:
            label = lod[0]["itemLabel"]
        return label

    def getClassQids(self, qids: list) -> dict:
        """
        get the Wikidata Q-Identifiers
        for the given wikidata ids

        Args:
            qids(list): the list of id
        """
        sparql_query = f"""# get the instanceof values for a given entity
SELECT ?item ?itemLabel ?qid ?class_qid ?class ?classLabel
WHERE 
{{
  VALUES ?item {{
"""
        for qid in qids:
            if not qid.startswith("http:"):
                wd_url = f"http://www.wikidata.org/entity/{qid}"
            else:
                wd_url = qid
            sparql_query += f"    <{wd_url}>\n"
        sparql_query += f"""}}
  ?item wdt:P31/wdt:P279* ?class.
  # labels may only exist as language independent mul - prefer en
  OPTIONAL {{ ?item rdfs:label ?itemEnLabel. FILTER(LANG(?itemEnLabel)="en") }}
  OPTIONAL {{ ?item rdfs:label ?itemMulLabel. FILTER(LANG(?itemMulLabel)="mul") }}
  BIND(COALESCE(?itemEnLabel, ?itemMulLabel) AS ?itemLabel)
  FILTER(BOUND(?itemLabel))
  OPTIONAL {{ ?class rdfs:label ?classEnLabel. FILTER(LANG(?classEnLabel)="en") }}
  OPTIONAL {{ ?class rdfs:label ?classMulLabel. FILTER(LANG(?classMulLabel)="mul") }}
  BIND(COALESCE(?classEnLabel, ?classMulLabel) AS ?classLabel)
  FILTER(BOUND(?classLabel))
  BIND(REPLACE(STR(?class),"http://www.wikidata.org/entity/","") AS ?class_qid)
  BIND(REPLACE(STR(?item),"http://www.wikidata.org/entity/","") AS ?qid)
}}"""
        if self.debug:
            print(sparql_query)
        class_rows = self.sparql.queryAsListOfDicts(sparql_query)
        class_map = LOD.getLookup(class_rows, "qid", withDuplicates=True)
        return class_map
