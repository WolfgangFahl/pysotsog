'''
Created on 2022-11-16

@author: wf
'''
import skg.graph
import os
import sys
import traceback
from skg.version import Version
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter


__version__ = Version.version
__date__ = Version.date
__updated__ = Version.updated

class Scholar(skg.graph.Node):
    """
    an instance of a scholar that writes papers to be an author
    """
    
    @classmethod
    def getSamples(cls):
        samples=[
            {"wikiDataId":"Q54303353",
             "gndId":"",
             "dblpId":"d/StefanDecker",
             "orcid":"0000-0001-6324-7164",
             "linkedInId":"",
             "googleScholarUser":"uhVkSswAAAAJ",
             "homepage":"http://www.stefandecker.org"
             }]
        return samples
        
    
    def __init__(self):
        """
        constructor
        """
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
        parser.add_argument("-d", "--debug", dest="debug", action="store_true", help="show debug info")
        parser.add_argument('-V', '--version', action='version', version=program_version_message)
        
        args = parser.parse_args(argv[1:])
        if len(argv) < 2:
            parser.print_usage()
            sys.exit(1)
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