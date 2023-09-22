'''
Created on 2022-11-16

@author: wf
'''
import sys
import webbrowser
from argparse import ArgumentParser
from skg.wdsearch import WikidataSearch
from skg.wikidata import Wikidata
from skg.smw import SemWiki
from skg.kg import SKG_Def
from skg.graph import Node
from skg.paper import Paper
from skg.doi import DOI
from skg.orcid import ORCID
from skg.crossref import Crossref
from skg.skgbrowser import SkgBrowser
from skg.search import SearchOptions, SearchResult
from ngwidgets.ngwidgets_cmd import WebserverCmd

class SotSog(WebserverCmd):
    """
    Standing on the shoulders of giants 
    """
    
    def __init__(self):
        """
        constructor
        
        """
        self.config=SkgBrowser.get_config()
        self.config.sotsog=self
        WebserverCmd.__init__(self, self.config, SkgBrowser, DEBUG)
        Node.debug=self.debug
        self.wikipedia_url="https://en.wikipedia.org/wiki/Standing_on_the_shoulders_of_giants"
        self.skg_def=SKG_Def()
        self.scholar_concept=self.skg_def.concepts["Scholar"]
    
    def getMarkups(self,item,options:SearchOptions)->dict:
        """
        get the markups for the given item and search options
        
        Args:
            item(Node): the item to get the markup for
            options(SearchOptions): the search options to apply
        """
        markups={}
        do_markup=len(options.markup_names)>0
        if do_markup:
            if item.concept.name=="Paper":
                doi=getattr(item, "doi",None)
                if doi is not None:
                    crossref=Crossref()
                    if "bibtex" in options.markup_names:
                        bibentry=crossref.doiBibEntry([doi])
                        markups["bibtex"]=bibentry
                    if "scite" in options.markup_names:
                        #meta_data=crossref.doiMetaData([doi])
                        #scite_entry=crossref.asScite(meta_data)
                        if not hasattr(item, "doi_obj"):
                            item.fromDOI(doi)
                        scite_entry=item.doi_obj.asScite()
                        markups["scite"]=scite_entry
            if item.concept.name=="Scholar":
                if "smw" in options.markup_names:
                    markups["smw"]=SemWiki.asMarkup(item)
        return markups
    
    def wd_search(self,wd:Wikidata,search_term:str,options)->list:
        """
        do a wikidata search
        """
        items=[]
        wds=WikidataSearch(language=options.lang,debug=self.debug)
        search_options=wds.searchOptions(search_term,limit=options.limit)
        qids=[]
        for qid,itemLabel,desc in search_options:
            qids.append(qid)
        class_map=wd.getClassQids(qids)
        for qid,itemLabel,desc in search_options:
            if qid in class_map:
                class_rows=class_map[qid]
                for class_row in class_rows:
                    class_qid=class_row["class_qid"]
                    concept=self.skg_def.conceptForQid(class_qid)
                    if concept is not None:
                        wd_items=concept.cls.from_wikidata_via_id(concept,"wikiDataId", qid, lang=options.lang)
                        if len(wd_items)>0:
                            item=wd_items[0]
                            items.append(item)
                            self.handleItem(item,qid,itemLabel,desc,options)
        return items                    
                            
    def handleItem(self,item,item_id,itemLabel,desc,options):
        """
        handle the given item as a search result
        """
        if options.show:
            print(f"{itemLabel}({item_id}):{desc}✅")
            print(item)
        item.markups=self.getMarkups(item,options)
        if options.show:
            for markup_name,markup in item.markups.items():
                print(f"{markup_name} markup:")
                print(markup)
            pass
        if options.open_browser:
            browser_url=item.browser_url()
            if browser_url is not None:
                print(f"opening {browser_url} in browser")
                webbrowser.open(browser_url)

    def handleItems(self,items,options):
        """
        handle the given items
        """
        for item in items:
            item_id=item.wikiDataId
            itemLabel=item.label
            desc="?"
            self.handleItem(item, item_id, itemLabel, desc, options)
            
    def handleDoiItem(self,item,options:SearchOptions):
        item_id=item.doi
        itemLabel=item.title
        desc=item.title
        self.handleItem(item, item_id, itemLabel, desc, options)
    
    def search(self,search_list,options:SearchOptions)->SearchResult:
        """
        search with the given search list
        
        Args:
            search_list(list): a list of search terms
            options(SearchOptions): the search options to apply
        """
        search_result=SearchResult(search_list,options)
        search_term=' '.join(search_list)
        for prefix in ["https://doi.org"]:
            if search_term.startswith(prefix):
                search_term=search_term.replace(prefix,"")
        wd=Wikidata(debug=self.debug)
        if ORCID.isORCID(search_term):
            scholar_concept=self.skg_def.concepts["Scholar"]
            items=Node.from_wikidata_via_id(scholar_concept, "orcid", search_term, options.lang)
            self.handleItems(items,options)
        elif DOI.isDOI(search_term):
            # DOI may not be referencing paper but something else
            paper_concept=self.skg_def.concepts["Paper"]
            items=Paper.from_wikidata_via_id(paper_concept, "doi", search_term, options.lang)
            self.handleItems(items,options)
            dblp_items=Paper.from_dblp_via_id(paper_concept, "doi", search_term.lower())
            if len(dblp_items)==0:
                paper=Paper()
                paper.concept=paper_concept
                paper.fromDOI(search_term)
                paper.provenance="doi"
                dblp_items=[paper]
            for item in dblp_items:
                self.handleDoiItem(item,options)
            items.extend(dblp_items)
        else:
            items=self.wd_search(wd,search_term,options)               
        search_result.items=items
        return search_result
    
    def getArgParser(self,description:str,version_msg)->ArgumentParser:
        """
        override the default argparser call
        """        
        parser=super().getArgParser(description, version_msg)
        parser.add_argument('search', action='store', nargs='*', help="search terms")
        parser.add_argument("--bibtex",help="output bibtex format",action="store_true")
        parser.add_argument("-la", "--lang",help="language code to use",default="en")
        parser.add_argument("-li", "--limit",help="limit the number of search results",type=int,default=9)
        parser.add_argument("-nb","--nobrowser",help="do not open browser",action="store_true")
        parser.add_argument("--scite",help="output #scite format",action="store_true")
        parser.add_argument("--smw",help="output Semantic MediaWiki (SMW) format",action="store_true")   
        parser.add_argument("--wikiId",help="the id of the SMW wiki to connect with",default="ceur-ws")
        return parser
    
    def handle_args(self)->bool:
        markup_names=[]
        args=self.args
        if args.bibtex: markup_names.append("bibtex")
        if args.scite: markup_names.append("scite")
        if args.smw: markup_names.append("smw")
        self.config.options=SearchOptions(limit=args.limit,lang=args.lang,
                      markup_names=markup_names,
                      open_browser=not args.nobrowser)
        handled=super().handle_args()
        if not handled:
            self.search(args.search,self.config.options)  
            handled=True
        return handled    
    
        
def main(argv:list=None):
    """
    main call
    """
    cmd=SotSog()
    exit_code=cmd.cmd_main(argv)
    return exit_code
        
DEBUG = 0
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    sys.exit(main())
