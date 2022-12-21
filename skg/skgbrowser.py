'''
Created on 2022-11-18

@author: wf
'''    
import html
import os
from jpcore.compat import Compatibility;Compatibility(0,11,1)
from jpcore.justpy_config import JpConfig
script_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = script_dir+"/resources/static"
JpConfig.set("STATIC_DIRECTORY",static_dir)
# shut up justpy
JpConfig.set("VERBOSE","False")
JpConfig.setup()
from jpwidgets.bt5widgets import App,Link,About
from urllib import parse
from skg.search import SearchOptions
from skg.orcid import ORCID
from wikibot3rd.wikiuser import WikiUser

class SkgBrowser(App):
    """
    scholary knowledge graph browser
    """
  
    def __init__(self,version,sotsog,options:SearchOptions):
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
        self.addMenuLink(text='Chat',icon='chat',href=version.chat_url)
        self.addMenuLink(text='Documentation',icon='file-document',href=version.doc_url)
        self.addMenuLink(text='Settings',icon='cog',href="/settings")
        self.addMenuLink(text='About',icon='information',href="/about")
        self.options=options
        self.markup_names=["-","bibtex","scite","smw"]
        self.markup_name=self.markup_names[1]
        # wiki users
        self.wikiUsers=WikiUser.getWikiUsers()
        self.wikiId="ceur-ws"
        jp.Route('/settings',self.settings)
        jp.Route('/about',self.about)
        
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
            
    async def onChangeMarkup(self,msg):
        """
        handle button to search for terms
        """
        try:
            self.markup_name=msg.value
        except Exception as ex:
            self.handleException(ex)
            
    def setupRowsAndCols(self):
        """
        setup the general layout
        """
        head_html="""<link rel="stylesheet" href="/static/css/md_style_indigo.css">"""
        self.wp=self.getWp(head_html)
        self.button_classes = """btn btn-primary"""
        # rows
        self.rowA=self.jp.Div(classes="row",a=self.contentbox)
        self.rowB=self.jp.Div(classes="row",a=self.contentbox)
        self.rowC=self.jp.Div(classes="row",a=self.contentbox)
        # columns
        self.colA1=self.jp.Div(classes="col-12",a=self.rowA)
        self.colB1=self.jp.Div(classes="col-6",a=self.rowB)
        self.rowB1r1=self.jp.Div(classes="row",a=self.colB1)
        self.colB11=self.jp.Div(classes="col-3",a=self.rowB1r1)
        self.rowB1r2=self.jp.Div(classes="row",a=self.colB1)
        self.colB12=self.jp.Div(classes="col-6",a=self.rowB1r2)
        self.colB2=self.jp.Div(classes="col-6",a=self.rowB)
        self.colC1=self.jp.Div(classes="col-12",a=self.rowC,style='color:black')
        # standard elements
        self.errors=self.jp.Div(a=self.colA1,style='color:red')
        self.messages=self.jp.Div(a=self.colC1,style='color:black')    
        
    async def onChangeLanguage(self,msg):
        """
        react on language being changed via Select control
        """
        self.language=msg.value  
        
    async def onChangeWikiUser(self,msg):
        """
        react on a the wikiuser being changed via a Select control
        """
        self.wikiId=msg.value
  
    def addLanguageSelect(self):
        """
        add a language selector
        """
        self.languageSelect=self.createSelect("Language","en",a=self.colB11,change=self.onChangeLanguage)
        for language in self.getLanguages():
            lang=language[0]
            desc=language[1]
            desc=html.unescape(desc)
            self.languageSelect.add(self.jp.Option(value=lang,text=desc))
            
    def addWikiUserSelect(self):
        """
        add a wiki user selector
        """
        if len(self.wikiUsers)>0:
            self.wikiuser_select=self.createSelect("wikiId", value=self.wikiId, change=self.onChangeWikiUser, a=self.colB11)
            for wikiUser in sorted(self.wikiUsers):
                self.wikiuser_select.add(self.jp.Option(value=wikiUser,text=wikiUser)) 
      
    async def settings(self)->"jp.WebPage":
        '''
        settings
        
        Returns:
            jp.WebPage: a justpy webpage renderer
        '''
        self.setupRowsAndCols()
        self.addLanguageSelect()
        self.addWikiUserSelect()
        return self.wp
    
    async def about(self)->"jp.WebPage":
        '''
        show about dialog
        
        Returns:
            jp.WebPage: a justpy webpage renderer
        '''
        self.setupRowsAndCols()
        self.aboutDiv=About(a=self.colB1,version=self.version)
        # @TODO Refactor to pyJustpyWidgets
        return self.wp
        
    async def content(self)->"jp.WebPage":
        '''
        provide the main content page
        
        Returns:
            jp.WebPage: a justpy webpage renderer
        '''
        self.setupRowsAndCols()
        self.results=self.jp.Div(a=self.colC1)
        self.markup=self.colB2
        # sotsog search
        self.markup_select = self.createSelect("markup",
            value=self.markup_name,
            change=self.onChangeMarkup,
            a=self.colB11)
        for markup_name in self.markup_names:
            self.markup_select.add(self.jp.Option(value=markup_name,text=markup_name))
        #self.conceptSelection=
        self.searchTerms=self.jp.Textarea(placeholder="enter search terms", a=self.colB12, rows=5,cols=120)
        self.searchButton=self.jp.Button(text="search",click=self.onSearchButton,a=self.colB12,classes=self.button_classes)
        return self.wp
    
    def start(self,host,port,debug):
        """
        start the server
        """
        self.debug=debug
        import justpy as jp
        jp.justpy(self.content,host=host,port=port)