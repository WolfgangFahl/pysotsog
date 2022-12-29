'''
Created on 2022-11-16

@author: wf
'''

import os
import webbrowser
import sys
import traceback
from skg.version import Version
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
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
from jpcore.justpy_app import JustpyServer

class SotSog():
    """
    Standing on the shoulders of giants
    """
    
    def __init__(self,args=None):
        """
        constructor
        
        Args:
            args(): command line Arguments(optional)
        """
        self.args=args
        debug=False
        if args:
            debug=args.debug
        self.debug=debug
        Node.debug=debug
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

__version__ = Version.version
__date__ = Version.date
__updated__ = Version.updated


def main(argv=None): # IGNORE:C0111
    '''main program.'''

    if argv is None:
        argv=sys.argv[1:]
    
    program_name = os.path.basename(__file__)
    program_shortdesc = Version.description
    
    program_version =f"v{__version__}" 
    program_build_date = str(__updated__)
    program_version_message = f'{program_name} ({program_version},{program_build_date})'

    user_name="Wolfgang Fahl"
    program_license = '''%s

  Created by %s on %s.
  Copyright 2022 Wolfgang Fahl. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, user_name,str(__date__))
    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('search', action='store', nargs='*', help="search terms")
        parser.add_argument("--about",help="show about info",action="store_true")
        parser.add_argument("--bibtex",help="output bibtex format",action="store_true")
        parser.add_argument("-d", "--debug", dest="debug", action="store_true", help="show debug info")
        parser.add_argument('--host',default=JustpyServer.getDefaultHost())
        parser.add_argument("-la", "--lang",help="language code to use",default="en")
        parser.add_argument("-li", "--limit",help="limit the number of search results",type=int,default=9)
        parser.add_argument("-nb","--nobrowser",help="do not open browser",action="store_true")
        parser.add_argument('--port',type=int,default=8765)
        parser.add_argument("--scite",help="output #scite format",action="store_true")
        parser.add_argument("--smw",help="output Semantic MediaWiki (SMW) format",action="store_true")   
        parser.add_argument("--serve",help="start webserver",action="store_true")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        args = parser.parse_args(argv)
        if len(argv) < 1:
            parser.print_usage()
            sys.exit(1)
        sotsog=SotSog(args)
        markup_names=[]
        if args.bibtex: markup_names.append("bibtex")
        if args.scite: markup_names.append("scite")
        if args.smw: markup_names.append("smw")
        options=SearchOptions(limit=args.limit,lang=args.lang,
                      markup_names=markup_names,
                      open_browser=not args.nobrowser)
        if args.about:
            print(program_version_message)
            print(f"see {Version.doc_url}")
            webbrowser.open(Version.doc_url)
        elif args.serve:
            skgBrowser=SkgBrowser(version=Version,sotsog=sotsog,options=options)
            url=f"http://{args.host}:{args.port}"
            webbrowser.open(url)
            skgBrowser.start(args.host, args.port,debug=args.debug)
            pass
        else:
            sotsog.search(args.search,options)
        pass
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 1
    except Exception as e:
        if DEBUG:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        if args.debug:
            print(traceback.format_exc())
        return 2       
        
DEBUG = 1
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    sys.exit(main())
