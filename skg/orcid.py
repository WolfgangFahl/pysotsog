'''
Created on 2022-11-19

@author: wf
'''
import requests
import re
from stdnum.iso7064.mod_11_2  import validate

class ORCID:
    """
    ORCID handling
    
    see e.g. 
        https://info.orcid.org/brand-guidelines/#h-orcid-logos-and-icons
        https://pub.orcid.org/v3.0/
    """
    pattern=re.compile(r"^(\d{4}-){3}\d{3}(\d|X)$")
    
    def __init__(self,orcid:str):
        """
        constructor
        
        Args:
            orcid(str): the orcid
        """
        self.orcid=orcid
        #https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier
        self.orcid_num=orcid.replace("-","")
        match=re.match(ORCID.pattern,orcid)
        self.ok=bool(match) and validate(self.orcid_num)
        
    @classmethod
    def isORCID(cls,orcid:str)->bool:
        """
        check that the given string is an ORCID
        
        Args:
            orcid(str): the potential ORCID string
            
        Returns:
            bool: True if the string represents a valid ORCID otherwise false
        """
        if not orcid:
            return False
        orcid_obj=ORCID(orcid)
        return orcid_obj.ok
        
    def getMetadata(self,op:str=None)->dict:
        """
        get the ORCID metadata data
        
        Args:
            op(str): the https://pub.orcid.org/v3.0/ API 
            operation to apply - default is "Fetch record details"
            
        Returns:
            dict: the dictionary derived from the JSON response
            
        """
        op="" if op is None else f"/{op}"
        url=f'https://pub.orcid.org/v3.0/{self.orcid}{op}'
        r = requests.get(url,
                            headers = {'User-Agent':'Mozilla/5.0', 'accept' : 'application/json'})
        json_data=r.json()
        return json_data
        
    def asHtml(self,mode:str="full",inline:str="")->str:
        """
        the orcid logo 
        
        Args:
            mode(str): the mode
            inline(str): in inline mode this is the text to be displayed inline 
            
        Returns:
            str: the html code
            
        """
        href=f"""https://orcid.org/{self.orcid}"""
        logo="""<img alt="ORCID logo" src="https://info.orcid.org/wp-content/uploads/2019/11/orcid_16x16.png" width="16" height="16" />"""
        if mode=="full":
            html=f"""<a href="{href}">{logo}{href}</a>"""
        elif mode=="compact":
            html=f"""<a href="{href}">{logo}{self.orcid}</a>"""
        elif mode=="inline":
            html=f"""<a href="{href}">{inline}{logo}</a>"""
        return html