"""
Created on 2023-01-04

@author: wf
"""
from typing import Callable

from lodstorage.sparql import SPARQL
from spreadsheet.wbquery import WikibaseQuery
from wd.wdgrid import GridSync, WikidataGrid

from skg.smw import SemWiki


class ScholarQuery:
    @classmethod
    def get(cls) -> WikibaseQuery:
        """
        get the WikiBaseQuery for scholars

        Returns:
            WikibaseQuery: the wikibase query
        """
        scholar_mapping = [
            # @TODO use metamodel info and read from wiki
            {
                "Column": "",
                "Entity": "Scholar",
                "Lookup": "",
                "PropVarname": "instanceof",
                "PropertyId": "P31",
                "PropertyName": "instanceof",
                "Qualifier": "",
                "Type": "",
                "Value": "Q5",
            },
            {
                "Column": "wikiDataId",
                "Entity": "Scholar",
                "Lookup": "",
                "PropVarname": "",
                "PropertyId": "",
                "PropertyName": "",
                "Qualifier": "",
                "Type": "item",
                "Value": "",
            },
            {
                "Column": "name",
                "Entity": "Scholar",
                "Lookup": "Q101352",
                "PropVarname": "family_name",
                "PropertyId": "P734",
                "PropertyName": "family name",
                "Qualifier": "",
                "Type": "",
                "Value": "",
            },
            {
                "Column": "firstName",
                "Entity": "Scholar",
                "Lookup": "Q202444",
                "PropVarname": "given_name",
                "PropertyId": "P735",
                "PropertyName": "given name",
                "Qualifier": "",
                "Type": "",
                "Value": "",
            },
            {
                "Column": "homepage",
                "Entity": "Scholar",
                "Lookup": "",
                "PropVarname": "official_website",
                "PropertyId": "P856",
                "PropertyName": "official website",
                "Qualifier": "",
                "Type": "url",
                "Value": "",
            },
            {
                "Column": "linkedInId",
                "Entity": "Scholar",
                "Lookup": "",
                "PropVarname": "LinkedIn_personal_profile_ID",
                "PropertyId": "P6634",
                "PropertyName": "LinkedIn personal profile ID",
                "Qualifier": "",
                "Type": "extid",
                "Value": "",
            },
            {
                "Column": "orcid",
                "Entity": "Scholar",
                "Lookup": "",
                "PropVarname": "ORCID_iD",
                "PropertyId": "P496",
                "PropertyName": "ORCID iD",
                "Qualifier": "",
                "Type": "extid",
                "Value": "",
            },
            {
                "Column": "googleScholarUser",
                "Entity": "Scholar",
                "Lookup": "",
                "PropVarname": "Google_Scholar_author_ID",
                "PropertyId": "P1960",
                "PropertyName": "Google Scholar author ID",
                "Qualifier": "",
                "Type": "extid",
                "Value": "",
            },
            {
                "Column": "researchGate",
                "Entity": "Scholar",
                "Lookup": "",
                "PropVarname": "ResearchGate_profile_ID",
                "PropertyId": "P2038",
                "PropertyName": "ResearchGate profile ID",
                "Qualifier": "",
                "Type": "extid",
                "Value": "",
            },
            {
                "Column": "gndId",
                "Entity": "Scholar",
                "Lookup": "",
                "PropVarname": "GND_ID",
                "PropertyId": "P227",
                "PropertyName": "GND ID",
                "Qualifier": "",
                "Type": "extid",
                "Value": "",
            },
            {
                "Column": "dblpId",
                "Entity": "Scholar",
                "Lookup": "",
                "PropVarname": "DBLP_author_ID",
                "PropertyId": "P2456",
                "PropertyName": "DBLP author ID",
                "Qualifier": "",
                "Type": "extid",
                "Value": "",
            },
        ]
        wbQuery = WikibaseQuery("scholar")
        for row in scholar_mapping:
            wbQuery.addPropertyFromDescriptionRow(row)
        return wbQuery


class SmwGrid(GridSync):
    """
    a semantic mediawiki based grid synchable with WikiData

    """

    def __init__(
        self,
        app,
        entityName: str,
        entityPluralName: str,
        pk: str,
        getLod: Callable,
        wikiUsers: list,
        wikiId: str,
        sparql: SPARQL,
        debug: bool = False,
    ):
        """
        constructor

        Args:
            app(App): the app that i am part of
            entityName(str): the name of the entity type of items to be shown in the grid
            entityPluralName(str): the plural name of the entities to be shown
            pk(str): the name of the primary key
            getLod(Callable): the callback to load the grid rows list of dicts
            wikiUsers(list): the wikiUsers
            wikiId(str): the wikiId to use
            sparql(SPARQL): the SPARQL endpoint to use
            debug(bool): if True show debugging information
        """
        self.app = app
        self.wikiUsers = wikiUsers
        self.wikiId = wikiId
        wikiUser = self.wikiUsers[wikiId]
        self.semwiki = SemWiki(wikiUser)
        wdGrid = WikidataGrid(
            app=app,
            source=wikiId,
            entityName=entityName,
            entityPluralName=entityPluralName,
            getLod=getLod,
            debug=debug,
        )
        # we'd rather lazy load
        # wdGrid.lod=wdGrid.getLod()
        super().__init__(wdGrid, entityName, pk, sparql=sparql, debug=debug)


class ScholarGrid(SmwGrid):
    """
    show a grid of scholars
    """

    def __init__(
        self, app, wikiUsers, wikiId: str, sparql: SPARQL, debug: bool = False
    ):
        """
        constructor

        Args:
            app(App): the app that I am part of
            wikiUsers(list): the wikiUsers
            wikiId(str): the wikiId to use
            sparql(SPARQL): the SPARQL endpoint to use
            debug(bool): if True show debugging information
        """
        entityName = "Scholar"
        entityPluralName = "Scholars"
        pk = "item"
        super().__init__(
            app=app,
            wikiUsers=wikiUsers,
            wikiId=wikiId,
            entityName=entityName,
            entityPluralName=entityPluralName,
            pk=pk,
            getLod=self.getScholars,
            sparql=sparql,
            debug=debug,
        )

    def getScholars(self) -> list:
        """
        get the list of scholars

        Returns:
            list: the list of dicts of scholars
        """
        # get a dict of dict
        scholars_dod = self.semwiki.scholars()
        # get a list of dicts
        scholars_lod = list(scholars_dod.values())
        # @TODO - shouldn't this be better specified in the mapping?
        for row in scholars_lod:
            row["label"] = row["Scholar"]
        self.wbQuery = ScholarQuery.get()
        return scholars_lod
