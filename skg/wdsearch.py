'''
Created on 24.07.2022

@author: wf
'''
import json
import os
import urllib.request
import urllib.parse

class WikidataSearch(object):
    '''
    Wikidata Search
    '''

    def __init__(self,language='en',timeout=2.0,debug:bool=False):
        '''
        Constructor
        
        Args:
            language(str): the language to use e.g. en/fr
            timeout(float): maximum time to wait for result
            debug(bool): if True debug details should be shown
        '''
        self.language=language
        self.timeout=timeout
        self.debug=debug
        
    def searchOptions(self,searchFor:str,limit:int=9)->list:
        '''
        search and return a list of qid,itemLabel description tuples
        
        Args:
            searchFor(str): the string to search for
            limit(int): the maximum amount of results to search for
        '''
        options=[]
        srlist=self.search(searchFor, limit)
        if srlist is not None:
            for sr in srlist:
                qid=sr["id"]
                itemLabel=sr["label"]
                desc=""
                if "display" in sr:
                    display=sr["display"]
                    if "description" in display:
                        desc=display["description"]["value"]
                options.append((qid,itemLabel,desc,))
        return options

    def search(self,searchFor:str,limit:int=9):
        '''
        
        Args:
            searchFor(str): the string to search for
            limit(int): the maximum amount of results to search for
        '''
        try:
            apiurl=f"https://www.wikidata.org/w/api.php?action=wbsearchentities&language={self.language}&format=json&limit={limit}&search="
            if self.debug:
                print(apiurl)
            searchEncoded=urllib.parse.quote_plus(searchFor)
            apisearch=apiurl+searchEncoded
            with urllib.request.urlopen(apisearch,timeout=self.timeout) as url:
                searchResult = json.loads(url.read().decode())
            return searchResult["search"]
        except Exception as _error:
            return None
        
    def getProperties(self):
        '''
        get the Wikidata Properties 
        '''
        scriptdir=os.path.dirname(__file__)
        jsonPath=f"{scriptdir}/resources/wdprops.json"
        with open(jsonPath) as jsonFile:
            props=json.load(jsonFile)
        return props