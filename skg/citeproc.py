'''
Created on 2022-12-21

@author: wf
'''
import datetime
class Citeproc:
    """
    see https://en.wikipedia.org/wiki/CiteProc
    """
    
    @classmethod
    def asScite(cls,meta_data:dict,retrieved_from:str)->str:
        """
        convert the given meta data to #Scite format
        
        see https://github.com/SemanticMediaWiki/SemanticCite/blob/master/src/FilteredMetadata/BibliographicFilteredRecord.php
        Args:
            meta_data(dict): the citeproc compatible metadata dict to convert
            retrieved_from(str): the url the metadata was retrieved from
            
        Returns:
            str: Semantic Mediawiki markup
        """
        def unlist(value):
            if type(value)!=list:
                return value
            text=""
            delim=""
            for item in value:
                text+=f"{delim}{item}"
                delim=";"
            if len(value)>1:
                text+="|+sep=;"
            return text
        
        def get_author(value)->str:
            """
            get the author markup
            
            Args:
                value(list): the list to disassemble
                
            Returns:
                str: Mediawiki markup
            """
            author=""
            delim=""
            for arec in value:
                author+= f"""{delim}{arec["given"]} {arec["family"]}"""
                delim=";"
            return author
        
        timestamp=datetime.datetime.utcnow().strftime('%Y-%m-%d')
        ref_type="journal-article"
        title=meta_data["title"]
        if type(title) is list:
            title=title[0]
        title_2=title.lower()[:2]
        author_lower=""
        if "author" in meta_data:
            author_lower=meta_data["author"][0]["family"].lower()
        year=""
        if "published-print" in meta_data:
            year=meta_data["published-print"]["date-parts"][0][0]
        if not year and "issued" in meta_data:
            year=meta_data["issued"]["date-parts"][0][0]
        reference=f"{author_lower}{year}{title_2}"
        markup=""
        for skey,mkey,func in [
            ("title","title",unlist),
            ("subtitle","subtitle",unlist),
            ("authors","author",get_author),
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
|retrieved-from={retrieved_from}
|retrieved-on={timestamp}
}}}}"""
        full_markup=f"{title}\n[[CiteRef::{reference}]]\n{markup}"
        return full_markup
