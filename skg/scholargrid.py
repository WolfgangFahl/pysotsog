'''
Created on 2023-01-04

@author: wf
'''
from jpwidgets.bt5widgets import Alert,IconButton

from skg.smw import SemWiki

import asyncio
import copy
import datetime
import json
import re
from typing import Callable

class WikiDataGrid:
    """
    show a grid of wiki data items
    """
    
    def __init__(self,source:str,entityName:str, entityPluralName:str,getLod:Callable,debug:bool=False):
        """
        constructor
        
        source(str): the name of my source (where the data for this grid comes from)
        entityName(str): the name of the entity type of items displayed in this grid
        entityPluralNam(str): the plural name of the entity type of items displayed in this grid
        getLod(Callable): the function to get my list of dicts
        debug(bool): if True show debugging information
        
        """
        self.debug=debug
        self.source=source
        self.entityName=entityName
        self.entityPluralName=entityPluralName
        self.getLod=getLod
        self.agGrid=None
        
    def setDefaultColDef(self, agGrid):
        """
        set the default column definitions
        """
        defaultColDef=agGrid.options.defaultColDef
        defaultColDef.resizable=True
        defaultColDef.sortable=True
        # https://www.ag-grid.com/javascript-data-grid/grid-size/
        defaultColDef.wrapText=True
        defaultColDef.autoHeight=True
        
    def setLod(self,lod:list):
        '''
        set my list of dicts
        
        Args:
            lod(list): a list of dicts to work with
        '''
        self.lod=lod
        if len(lod)<1:
            raise Exception("Empty List of dicts is not valid")
        self.columns=self.lod[0].keys()
        for index,row in enumerate(self.lod):
            row["lodRowIndex"]=index
        self.viewLod=copy.deepcopy(self.lod)
        
        # fix non values
        for record in self.viewLod:
            for key in list(record):
                value=record[key]
                if value is None:
                    record[key]="-"
                vtype=type(value)
                # fix datetime entries
                if vtype is datetime.datetime:
                    value=str(value)
                    record[key]=value
        
    def linkWikidataItems(self,viewLod,itemColumn:str="item"):
        '''
        link the wikidata entries in the given item column if containing Q values
        
        Args:
            viewLod(list): the list of dicts for the view
            itemColumn(str): the name of the column to handle
        '''
        for row in viewLod:
            if itemColumn in row:
                item=row[itemColumn]
                if re.match(r"Q[0-9]+",item):
                    itemLink=self.createLink(f"https://www.wikidata.org/wiki/{item}", item)
                    row[itemColumn]=itemLink
                    
    async def reload(self,_msg=None,clearErrors=True):
        '''
        reload the table content via my getLod function
        
        Args:
            clearErrors(bool): if True clear Errors before reloading
        '''
        try:
            if clearErrors:
                self.app.clearErrors()
            
            msg=f"reload called ... fetching scholars from {self.source}"
            print(msg)
            _alert=Alert(a=self.app.colB1,text=msg)
            await self.app.wp.update()
            items=self.getLod()
            self.setLod(items)
 
            _alert.delete_alert({})
            msg=f"found {len(items)} {self.entityPluralName}"
            _alert=Alert(a=self.app.colB1,text=msg)
            await self.app.wp.update()
            print(json.dumps(self.viewLod,indent=2,default=str))
            self.agGrid.load_lod(self.viewLod)
            self.setDefaultColDef(self.agGrid)
            self.agGrid.options.columnDefs[0].checkboxSelection = True
            # @FIXME
            self.agGrid.html_columns = [0, 1, 2,3]
            #self.agGrid.on('rowSelected', self.onRowSelected)
            await self.app.wp.update()
            await asyncio.sleep(0.2)
            await self.agGrid.run_api('sizeColumnsToFit()', self.app.wp)
        except Exception as ex:
            _error=self.app.jp.Span(a=_alert,text=f"Error: {str(ex)}",style="color:red")
            self.app.handleException(ex)           

class ScholarGrid(WikiDataGrid):
    """
    show a grid of scholars
    """
    
    def __init__(self,app,wikiUsers,wikiId:str,debug: bool = False):
        """
        constructor
        
        Args:
            app(App): the app that i am part of
            wikiUsers(list): the wikiUsers
            wikiId(str): the wikiId to use
            debug(bool): if True show debugging information
        """
        WikiDataGrid.__init__(self,source=wikiId,entityName="scholar",entityPluralName="scholars",getLod=self.getScholars,debug=debug)
        self.app=app
        self.wikiUsers=wikiUsers
        self.wikiId=wikiId
        wikiUser=self.wikiUsers[wikiId]
        self.semwiki=SemWiki(wikiUser)
        if app is not None:
            #self.app.wp.on("page_ready", self.pageReady)
            self.toolbar=self.app.jp.QToolbar(a=self.app.rowA)
            self.reloadButton=IconButton(a=self.toolbar,text='',iconName="refresh-circle",click=self.reload,classes="btn btn-primary btn-sm col-1")
            self.agGrid = self.app.jp.AgGrid(a=self.app.colC1)
        
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
        return scholars_lod