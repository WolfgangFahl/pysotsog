'''
Created on 2023-01-04

@author: wf
'''
from jpwidgets.bt5widgets import Alert,IconButton

from skg.smw import SemWiki
import json
import datetime
import asyncio

class ScholarGrid:
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
        self.app=app
        self.debug=debug
        self.agGrid=None
        self.wikiUsers=wikiUsers
        self.wikiId=wikiId
        wikiUser=self.wikiUsers[wikiId]
        self.semwiki=SemWiki(wikiUser)
        if app is not None:
            self.app.wp.on("page_ready", self.pageReady)
            self.toolbar=self.app.jp.QToolbar(a=self.app.rowA)
            self.reloadButton=IconButton(a=self.toolbar,text='',iconName="refresh-circle",click=self.reload,classes="btn btn-primary btn-sm col-1")
            self.agGrid = self.app.jp.AgGrid(a=self.app.colC1)
            
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
        
    def getScholars(self):
        """
        get the list of scholars 
        """
        scholars=self.semwiki.scholars()
        # fix non values
        for record in scholars.values():
            for key in list(record):
                value=record[key]
                if value is None:
                    record[key]="-"
                vtype=type(value)
                if vtype is datetime.datetime:
                    value=str(value)
                    record[key]=value
        return scholars
    
    async def reload(self,_msg=None,clearErrors=True):
        '''
        reload the table content from myl url and sheet name
        '''
        try:
            if clearErrors:
                self.app.clearErrors()
            
            msg=f"reload called ... fetching scholars from {self.app.wikiId}"
            print(msg)
            _alert=Alert(a=self.app.colB1,text=msg)
            await self.app.wp.update()
            scholars=self.getScholars()
            _alert.delete_alert({})
            lod=list(scholars.values())
            msg=f"found {len(lod)} scholars"
            _alert=Alert(a=self.app.colB1,text=msg)
            await self.app.wp.update()
            print(json.dumps(lod,indent=2,default=str))
            self.agGrid.load_lod(lod)
            self.setDefaultColDef(self.agGrid)
            self.agGrid.options.columnDefs[0].checkboxSelection = True
            self.agGrid.html_columns = [0, 1, 2,3]
            #self.agGrid.on('rowSelected', self.onRowSelected)
            await self.app.wp.update()
            await asyncio.sleep(0.2)
            await self.agGrid.run_api('sizeColumnsToFit()', self.app.wp)
        except Exception as ex:
            _error=self.app.jp.Span(a=_alert,text=f"Error: {str(ex)}",style="color:red")
            self.app.handleException(ex)
        
    async def pageReady(self,_msg):
        """
        react on page ready
        """
        await self.reload()
        pass
        
