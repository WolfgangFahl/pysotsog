'''
Created on 2023-01-04

@author: wf
'''
from skg.smw import SemWiki
from wd.wdgrid import  WikidataGrid,GridSync    
from spreadsheet.wbquery import WikibaseQuery
from lodstorage.sparql import SPARQL

class ScholarQuery():
    @classmethod 
    def get(cls)->WikibaseQuery:
        """
        get the WikiBaseQuery for scholars
        
        Returns:
            WikibaseQuery: the wikibase query
        """
        scholar_mapping=[
            # @TODO use metamodel info and read from wiki
            {'Column': '',
              'Entity': 'Scholar',
              'Lookup': '',
              'PropVarname': 'instanceof',
              'PropertyId': 'P31',
              'PropertyName': 'instanceof',
              'Qualifier': '',
              'Type': '',
              'Value': 'Q5'},
             {'Column': 'name',
              'Entity': 'Scholar',
              'Lookup': 'Q101352',
              'PropVarname': 'family_name',
              'PropertyId': 'P734',
              'PropertyName': 'family name',
              'Qualifier': '',
              'Type': '',
              'Value': ''},
             {'Column': 'firstName',
              'Entity': 'Scholar',
              'Lookup': 'Q202444',
              'PropVarname': 'given_name',
              'PropertyId': 'P735',
              'PropertyName': 'given name',
              'Qualifier': '',
              'Type': '',
              'Value': ''},
             {'Column': 'homepage',
              'Entity': 'Scholar',
              'Lookup': '',
              'PropVarname': 'official_website',
              'PropertyId': 'P856',
              'PropertyName': 'official website',
              'Qualifier': '',
              'Type': 'url',
              'Value': ''},
             {'Column': 'linkedInId',
              'Entity': 'Scholar',
              'Lookup': '',
              'PropVarname': 'LinkedIn_personal_profile_ID',
              'PropertyId': 'P6634',
              'PropertyName': 'LinkedIn personal profile ID',
              'Qualifier': '',
              'Type': 'extid',
              'Value': ''},
             {'Column': 'orcid',
              'Entity': 'Scholar',
              'Lookup': '',
              'PropVarname': 'ORCID_iD',
              'PropertyId': 'P496',
              'PropertyName': 'ORCID iD',
              'Qualifier': '',
              'Type': 'extid',
              'Value': ''},
             {'Column': 'googleScholarUser',
              'Entity': 'Scholar',
              'Lookup': '',
              'PropVarname': 'Google_Scholar_author_ID',
              'PropertyId': 'P1960',
              'PropertyName': 'Google Scholar author ID',
              'Qualifier': '',
              'Type': 'extid',
              'Value': ''},
             {'Column': 'gndId',
              'Entity': 'Scholar',
              'Lookup': '',
              'PropVarname': 'GND_ID',
              'PropertyId': 'P227',
              'PropertyName': 'GND ID',
              'Qualifier': '',
              'Type': 'extid',
              'Value': ''},
             {'Column': 'dblpId',
              'Entity': 'Scholar',
              'Lookup': '',
              'PropVarname': 'DBLP_author_ID',
              'PropertyId': 'P2456',
              'PropertyName': 'DBLP author ID',
              'Qualifier': '',
              'Type': 'extid',
              'Value': ''}
        ]
        wbQuery=WikibaseQuery("scholar")
        for row in scholar_mapping:
            wbQuery.addPropertyFromDescriptionRow(row)
        return wbQuery


class ScholarGrid(GridSync):
    """
    show a grid of scholars
    """
    
    def __init__(self,app,wikiUsers,wikiId:str,sparql:SPARQL,debug: bool = False):
        """
        constructor
        
        Args:
            app(App): the app that i am part of
            wikiUsers(list): the wikiUsers
            wikiId(str): the wikiId to use
            sparql(SPARQL): the SPARQL endpoint to use
            debug(bool): if True show debugging information
        """
        self.app=app
        self.wikiUsers=wikiUsers
        self.wikiId=wikiId
        wikiUser=self.wikiUsers[wikiId]
        self.semwiki=SemWiki(wikiUser)
        wdGrid=WikidataGrid(app=app,source=wikiId,entityName="scholar",entityPluralName="scholars",getLod=self.getScholars,debug=debug)
        # we'd rather lazy load
        wdGrid.lod=wdGrid.getLod()
        sheetName="Scholar"
        pk="item"
        GridSync.__init__(self, wdGrid, sheetName, pk, sparql=sparql,debug=debug)
        
    def getScholars(self)->list:
        """
        get the list of scholars 
        
        Returns:
            list: the list of dicts of scholars
        """
        # get a dict of dict
        scholars_dod=self.semwiki.scholars()
        # get a list of dicts
        scholars_lod=list(scholars_dod.values())
        self.wbQuery=ScholarQuery.get()
        return scholars_lod