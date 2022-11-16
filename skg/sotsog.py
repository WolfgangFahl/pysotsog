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
from skg.kg import SKG_Def
from skg.scholar import Scholar

class SotSog():
    """
    Standing on the shoulders of giants
    """
    
    def __init__(self):
        """
        constructor
        """
        self.wikipedia_url="https://en.wikipedia.org/wiki/Standing_on_the_shoulders_of_giants"
        self.skg_def=SKG_Def()
        self.scholar_concept=self.skg_def.concepts["Scholar"]
    
    def search(self,search_list,lang='en',show:bool=True,open_browser:bool=False)->list:
        """
        search with the given search list
        """
        search_term=' '.join(search_list)
        wd=WikidataSearch(language=lang)
        search_options=wd.searchOptions(search_term)
        scholars=[]
        for qid,itemLabel,desc in search_options:
            wd_scholars=Scholar.from_wikidata_via_id(self.scholar_concept,"wikiDataId", qid, lang=lang)
            if len(wd_scholars)>0:
                scholar=wd_scholars[0]
                scholars.append(scholar)
                if show:
                    print(f"{itemLabel}({qid}):{desc}✅")
                    print(scholar)
                if open_browser:
                    scholia_url=scholar.scholia_url()
                    print(f"opening {scholia_url} in browser")
                    webbrowser.open(scholia_url)
        return scholars

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
        sotsog=SotSog()
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
