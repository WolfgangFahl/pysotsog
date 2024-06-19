"""
Created on 2024-02-26

@author: wf
"""
from argparse import Namespace


class Dblp2Wikidata:
    """
    utility for transfering Dblp person entries to Wikidata
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        pass

    def transfer(self, args: Namespace):
        """
        Main method to handle the transfer of DBLP entries to Wikidata.

        Args:
            args(Namespace): Command line arguments.
        """
        search_term = getattr(args, "dblp2wikidata", None)
        if self.debug:
            print(f"trying to synchronize DBLP person entry for {search_term}")
