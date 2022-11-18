'''
Created on 2022-11-18

@author: wf
'''    
import os
from jpcore.compat import Compatibility;Compatibility(0,11,1)
from jpcore.justpy_config import JpConfig
script_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = script_dir+"/resources/static"
JpConfig.set("STATIC_DIRECTORY",static_dir)
JpConfig.setup()
from jpwidgets.bt5widgets import App,Link
from urllib import parse

class SkgBrowser(App):
    """
    scholary knowledge graph browser
    """
  
    def __init__(self,version,sotsog):
        '''
        Constructor
        
        Args:
            version(Version): the version info for the app
        '''
        self.sotsog=sotsog
        import justpy as jp
        self.jp=jp
        App.__init__(self, version)
        self.addMenuLink(text='Home',icon='home', href="/")
        self.addMenuLink(text='github',icon='github', href=version.cm_url)
        self.addMenuLink(text='Documentation',icon='file-document',href=version.doc_url)
        
    def createItemLink(self,item,term:str,index:int)->str:
        """
        create a link for the given item
        
        Args:
            item(Node): the item to create a link for
            term(str): the
        """
        if index>0:
            style="color:grey"
            text=f"{term}<sub>{index+1}</sub>"
            delim="&nbsp"
        else:
            style=""
            text=term
            delim=""
        markup=delim+Link.create(item.scholia_url(),text,tooltip=item.label,target="_blank",style=style)
        return markup      
        
    async def onSearchButton(self,_msg):
        """
        handle button to search for terms
        """
        try:
            self.results.inner_html=""
            terms=self.searchTerms.value.split("\n")
            self.messages.text="Searching"
            await self.wp.update()
            delim=""
            for term in terms:
                if term:
                    msg=f"... {term}\n"
                    self.messages.text+=msg
                    await self.wp.update()
                    items=self.sotsog.search([term],open_browser=self.sotsog.args.nobrowser)
                    markup=""
                    if len(items)==0:
                        # TODO check google search
                        # https://pypi.org/project/googlesearch-python/
                        params=parse.urlencode({'q':term})
                        search_url=f"https://www.google.com/search?{params}"
                        markup=Link.create(search_url, term, "not found", target="_blank",style="color:red")
                    else:
                        for i,item in enumerate(items):
                            markup+=self.createItemLink(item,term,i)
                    self.results.inner_html+=delim+markup  
                    delim="<br>" 
                    await self.wp.update()
            
        except Exception as ex:
            self.handleException(ex)
        
    async def content(self):
        '''
        show the content
        '''
        head_html="""<link rel="stylesheet" href="/static/css/md_style_indigo.css">"""
        self.wp=self.getWp(head_html)
        button_classes = """btn btn-primary"""
        self.rowA=self.jp.Div(classes="row",a=self.contentbox)
        self.rowB=self.jp.Div(classes="row",a=self.contentbox)
        self.rowC=self.jp.Div(classes="row",a=self.contentbox)
        self.colA1=self.jp.Div(classes="col-12",a=self.rowA)
        self.colB1=self.jp.Div(classes="col-3",a=self.rowB)
        self.colC1=self.jp.Div(classes="col-12",a=self.rowC,style='color:black')
        self.errors=self.jp.Div(a=self.colA1,style='color:red')
        self.messages=self.jp.Div(a=self.colC1,style='color:black')
        self.results=self.jp.Div(a=self.colC1)
        self.searchTerms=self.jp.Textarea(placeholder="enter search terms", a=self.colB1, rows=5,cols=160)
        self.searchButton=self.jp.Button(text="search",click=self.onSearchButton,a=self.colB1,classes=button_classes)
        return self.wp
    
    def start(self,host,port,debug):
        """
        start the server
        """
        self.debug=debug
        import justpy as jp
        jp.justpy(self.content,host=host,port=port)