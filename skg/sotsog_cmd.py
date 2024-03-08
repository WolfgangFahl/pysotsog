'''
Created on 2024-02-26

@author: wf
'''
import sys
from argparse import ArgumentParser
from skg.sotsog import SotSog, SearchOptions
from skg.dblp2wikidata import Dblp2Wikidata
from skg.skgbrowser import SkgBrowser

from ngwidgets.ngwidgets_cmd import WebserverCmd

class SotSogCmd(WebserverCmd):
    """
    command line handling for Standing on the Shoulders of Giants 
    """
    
    def __init__(self):
        self.config = SkgBrowser.get_config()
        WebserverCmd.__init__(self, self.config, SkgBrowser, DEBUG)

    def getArgParser(self, description: str, version_msg) -> ArgumentParser:
        """
        override the default argparser call
        """
        parser = super().getArgParser(description, version_msg)
        parser.add_argument("search", action="store", nargs="*", help="search terms")
        parser.add_argument(
            "--bibtex", help="output bibtex format", action="store_true"
        )
        parser.add_argument("-la", "--lang", help="language code to use", default="en")
        parser.add_argument(
            "-li",
            "--limit",
            help="limit the number of search results",
            type=int,
            default=9,
        )
        parser.add_argument(
            "-nb", "--nobrowser", help="do not open browser", action="store_true"
        )
        parser.add_argument("--scite", help="output #scite format", action="store_true")
        parser.add_argument(
            "--smw", help="output Semantic MediaWiki (SMW) format", action="store_true"
        )
        parser.add_argument(
            "--wikiId", help="the id of the SMW wiki to connect with", default="ceur-ws"
        )
        parser.add_argument("-dw","--dblp2wikidata", action="store_true", help="Transfer DBLP entries to Wikidata")
 
        return parser

    def handle_args(self) -> bool:
        """
        handle the command line args
        """
        markup_names = []
        args = self.args
        self.sotsog = SotSog(debug=args.debug)
        if args.bibtex:
            markup_names.append("bibtex")
        if args.scite:
            markup_names.append("scite")
        if args.smw:
            markup_names.append("smw")
        self.sotsog.options = SearchOptions(
            limit=args.limit,
            lang=args.lang,
            markup_names=markup_names,
            open_browser=not args.nobrowser,
        )
        handled = super().handle_args()
        if not handled:
            if args.dblp2wikidata:
                d2w=Dblp2Wikidata()
                d2w.transfer(args)
            self.search(args.search, self.sotsog.options)
            handled = True
        return handled

def main(argv: list = None):
    """
    main call
    """
    cmd = SotSogCmd()
    exit_code = cmd.cmd_main(argv)
    return exit_code


DEBUG = 0
if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-d")
    sys.exit(main())