'''
Created on 17.11.2022

@author: wf
'''
import skg
import datetime
import habanero
import habanero.cn as cn

class Crossref:
    """
    Crossref access
    """
    
    def __init__(self,mailto=None,ua_string=None):
        """
        constructor
        """
        if mailto is None:
            mailto="wf@bitplan.com"
        if ua_string is None:
            ua_string=f"pysotsog/{skg.__version__} (https://pypi.org/project/pysotsog/; mailto:{mailto})"
        self.cr = habanero.Crossref(mailto=mailto,ua_string=ua_string)  
    
    def doiMetaData(self, dois:list):
        """ 
        get the meta data for the given dois
        
        Args:
            doi(list): a list of dois
        """
        metadata = None
        response = self.cr.works(ids=dois)
        if 'status' in response and 'message' in response and response['status'] == 'ok':
            metadata = response['message']
        return metadata
    
    def doiBibEntry(self,dois:list):
        """
        get bib entries for the given dois
        """
        bibentry=cn.content_negotiation(ids = dois, format = "bibentry")
        return bibentry
    
    def asScite(self,meta_data:dict):
        """
        convert the given meta data to #Scite format
        
        see https://github.com/SemanticMediaWiki/SemanticCite/blob/master/src/FilteredMetadata/BibliographicFilteredRecord.php
        """
        def unlist(value):
            text=""
            delim=""
            for item in value:
                text+=f"{delim}{item}"
                delim=";"
            if len(value)>1:
                text+="|+sep=;"
            return text
        
        def get_author(value):
            author=""
            delim=""
            for arec in value:
                author+= f"""{delim}{arec["given"]} {arec["family"]}"""
                delim=";"
            return author
        
        timestamp=datetime.datetime.utcnow().strftime('%Y-%m-%d')
        ref_type="journal-article"
        title_2=meta_data["title"][0].lower()[:2]
        author_lower=meta_data["author"][0]["family"].lower()
        year=meta_data["published-print"]["date-parts"][0][0]
        reference=f"{author_lower}{year}{title_2}"
        markup=""
        for skey,mkey,func in [
            ("title","title",unlist),
            ("subtitle","subtitle",unlist),
            ("author","author",get_author),
            ("journal","container-title",unlist),
            ("publisher","publisher",str),
            ("issn","ISSN",unlist),
            ("subject","subject",unlist),
            ("volume","volume",str),
            ("pages","page",str),
            ("doi","DOI",str)
        ]:
            if mkey in meta_data:
                value=meta_data[mkey]
                if value:
                    value=func(value)
                    markup+=f"\n|{skey}={value}"
        markup=f"""{{{{#scite:
|reference={reference}
|type={ref_type}{markup}
|year={year}
|retrieved-from=https://dx.doi.org/
|retrieved-on={timestamp}
}}}}"""
        return markup