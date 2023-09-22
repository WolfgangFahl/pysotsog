'''
Created on 2022-11-18

@author: wf
'''    
from nicegui import ui, Client
from ngwidgets.input_webserver import InputWebserver
from ngwidgets.webserver import WebserverConfig
from ngwidgets.widgets import Link, Lang
from urllib import parse
from skg.orcid import ORCID
from skg.scholargrid import ScholarGrid
from wikibot3rd.wikiuser import WikiUser
from skg.wikidata import Wikidata
from skg.version import Version

class SkgBrowser(InputWebserver):
    """
    scholary knowledge graph browser
    """

    @classmethod
    def get_config(cls)->WebserverConfig:
        copy_right="(c)2022 Wolfgang Fahl"
        if not hasattr(cls, "config"):
            cls.config=WebserverConfig(copy_right=copy_right,version=Version(),default_port=8765)
        return cls.config
   
    def __init__(self):
        """Constructs all the necessary attributes for the WebServer object."""
        config=SkgBrowser.get_config()
        self.sotsog=config.sotsog
        self.options=config.options     
        InputWebserver.__init__(self,config=config)
        self.language="en"
        self.wikiId="or"
        self.markup_name=None
        
    def configure_run(self):
        self.markup_names=["-","bibtex","scite","smw"]
        self.markup_name=self.markup_names[1]
        # wiki users
        self.wikiUsers=WikiUser.getWikiUsers()
        self.wikiId=self.args.wikiId
        wikidata=Wikidata()
        self.sparql=wikidata.sparql
        
        @ui.page('/scholars')
        async def scholars(client: Client):
            return await self.scholars(client)
  
    def configure_menu(self):
        """
        configure additional non-standard menu entries
        """
        #self.link_button(name='Scholars',icon_name='account-school',target='/scholars')       
        pass
    
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
        link=Link.create(item.browser_url(),text,tooltip=item.label,target="_blank",style=style)
        if item.concept.name=="Scholar":
            if hasattr(item,"orcid"):
                orcid=ORCID(item.orcid)
                link+=orcid.asHtml()
        markup=delim+link
        return markup      
        
    async def onSearchButton(self,_msg):
        """
        handle button to search for terms
        """
        try:
            self.results.inner_html=""
            self.markup.inner_html=""
            terms=self.searchTerms.value.split("\n")
            self.messages.text="Searching"
            await self.wp.update()
            delim=""
            for term in terms:
                if term:
                    msg=f"... {term}\n"
                    self.messages.text+=msg
                    await self.wp.update()
                    if self.markup_name=="-":
                        self.options.markup_names=[]
                    else:
                        self.options.markup_names=[self.markup_name]
                    search_result=self.sotsog.search([term],self.options)
                    items=search_result.items
                    rmarkup=""
                    if len(items)==0:
                        # TODO check google search
                        # https://pypi.org/project/googlesearch-python/
                        params=parse.urlencode({'q':term})
                        search_url=f"https://www.google.com/search?{params}"
                        rmarkup=Link.create(search_url, term, "not found", target="_blank",style="color:red")
                    else:
                        for i,item in enumerate(items):
                            rmarkup+=self.createItemLink(item,term,i)
                            if len(item.markups)>0:
                                markups=""
                                for _markup_name,markup in item.markups.items():
                                    markups+=markup
                                    self.markup.inner_html+=f"<pre>{markups}</pre>"
                                    #break
                    self.results.inner_html+=delim+rmarkup  
                    delim="<br>" 
                    await self.wp.update()
            
        except Exception as ex:
            self.handleException(ex)
  
    def addLanguageSelect(self):
        """
        add a language selector
        """
        lang_dict=Lang.get_language_dict()
        self.add_select("language:",lang_dict).bind_value(self, "language")
           
    def addWikiUserSelect(self):
        """
        add a wiki user selector
        """
        if len(self.wikiUsers)>0:
            wu_dict={}
            for wikiUser in sorted(self.wikiUsers):
                wu_dict[wikiUser]=wikiUser
            self.add_select("wiki:",wu_dict).bind_value(self,"wikiId")
      
    async def scholars(self,client:Client):
        '''
        scholar display
        
        '''
        self.setup_menu()
        with ui.element("div").classes("w-full h-full"):
            try:
                self.scholarsGrid=ScholarGrid(self,self.wikiUsers,self.wikiId,sparql=self.sparql)
                # @TODO refactor the two setup calls to one to hide wdgrid details
                #self.scholarsGrid.setup(a=self.rowB, header=self.rowA)
                #self.scholarsGrid.wdgrid.setup(a=self.rowC)
            except BaseException as ex:
                self.handle_exception(ex) 
        await self.setup_footer()
    
    def configure_settings(self):
        """
        configure settings
        """
        self.addLanguageSelect()
        self.addWikiUserSelect()
        
    async def home(self,_client:Client):
        '''
        provide the main content page
        
        '''
        self.setup_menu()
        with ui.element("div").classes("w-full h-full"):
            self.results=ui.element("div")
            self.add_select("markup", self.markup_names).bind_value(self,"markup_name")
            #value=self.markup_name,
            #change=self.onChangeMarkup,
            #a=self.colB11)
            #self.conceptSelection=
            self.searchTerms=ui.textarea(placeholder="enter search terms")
            self.searchButton=ui.button("search",on_click=self.onSearchButton)
        await self.setup_footer()