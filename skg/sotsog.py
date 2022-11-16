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
from skg.kg import SKG_Def
from skg.graph import Node
from skg.scholar import Scholar

class SotSog():
    """
    Standing on the shoulders of giants
    """
    
    def __init__(self,debug:bool=False):
        """
        constructor
        
        Args:
            debug(bool): if True debugging should be switched on
        """
        self.debug=debug
        Node.debug=debug
        self.wikipedia_url="https://en.wikipedia.org/wiki/Standing_on_the_shoulders_of_giants"
        self.skg_def=SKG_Def()
        self.scholar_concept=self.skg_def.concepts["Scholar"]
    
    def search(self,search_list,lang='en',show:bool=True,open_browser:bool=False)->list:
        """
        search with the given search list
        """
        search_term=' '.join(search_list)
        wd=Wikidata()
        wds=WikidataSearch(language=lang,debug=self.debug)
        search_options=wds.searchOptions(search_term)
        items=[]
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
                        wd_items=concept.cls.from_wikidata_via_id(concept,"wikiDataId", qid, lang=lang)
                        if len(wd_items)>0:
                            item=wd_items[0]
                            items.append(item)
                            if show:
                                print(f"{itemLabel}({qid}):{desc}✅")
                                print(item)
                            if open_browser:
                                scholia_url=item.scholia_url()
                                print(f"opening {scholia_url} in browser")
                                webbrowser.open(scholia_url)
        return items

__version__ = Version.version
__date__ = Version.date
__updated__ = Version.updated


def main(argv=None): # IGNORE:C0111
    '''main program.'''

    if argv is None:
        argv=sys.argv[1:]
    
    program_name = os.path.basename(__file__)
    program_shortdesc = Version.description
    
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)

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
        parser.add_argument("-d", "--debug", dest="debug", action="store_true", help="show debug info")
        parser.add_argument("-l", "--lang",help="language code to use",default="en")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        args = parser.parse_args(argv)
        if len(argv) < 2:
            parser.print_usage()
            sys.exit(1)
        sotsog=SotSog(debug=args.debug)
        sotsog.search(args.search,lang=args.lang,open_browser=True)
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
