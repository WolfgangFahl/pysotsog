'''
Created on 2022-11-22

@author: wf
'''
from tests.basetest import Basetest
from skg.doi import DOI
from skg.smw import SemWiki
from wikibot3rd.wikiuser import WikiUser
import json
from collections import Counter

class TestSMW(Basetest):
    """
    test Semantic Mediawiki access
    """
    
    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.wikiUsers=WikiUser.getWikiUsers()
        
    
    def checkWikis(self,wikis,accessor,verbose:bool=True,debug:bool=False):
        """
        check the given wikis
        
        Args:
            wikis(list): a list of wikiId,withLogin tuples
            accessor(func): the function to check
            verbose(bool): if True show verbose details
            debug(bool): if True show debugging information
        """
        doiCounter=Counter()
        records=None
        for wikiId,withLogin in wikis:
            if wikiId in self.wikiUsers:
                wikiUser=self.wikiUsers[wikiId]
                semwiki=SemWiki(wikiUser,withLogin=withLogin)
                records=accessor(semwiki)
                if verbose:
                    print(f"found {len(records)} {accessor.__name__} references in {wikiId}" )
                if debug:
                    print(json.dumps(records,indent=2,default=str))
                for key,record in records.items():
                    if "doi" in record:
                        doi=record["doi"]
                        if doi:
                            self.assertTrue(DOI.isDOI(doi),f"{key}:doi={doi}")
                            doiCounter[wikiId]+=1
        if verbose:
            print(doiCounter.most_common())
        return records
    
    def test_dois(self):
        """
        test doi access
        """
        debug=self.debug
        wikis=[("confident","False)")]
        self.checkWikis(wikis,SemWiki.id_refs,debug=debug)
               
    def test_papers(self):
        """
        test getting paper references from a Semantic MediaWiki
        """
        debug=self.debug
        wikis=[("ceur-ws",False),("rq",True),("media",True)]
        self.checkWikis(wikis,accessor=SemWiki.papers,debug=debug)
                
    def test_scholars(self):
        """
        check access to scholars
        """
        debug=self.debug
        #debug=True
        wikis=[("media",True)]
        self.checkWikis(wikis,accessor=SemWiki.scholars,debug=debug)  
            
        
    
