'''
Created on 2022-11-19

@author: wf
'''
class ORCID:
    """
    ORCID handling
    see e.g. https://info.orcid.org/brand-guidelines/#h-orcid-logos-and-icons
    """
    def __init__(self,orcid:str):
        """
        constructor
        
        Args:
            orcid(str): the orcid
        """
        self.orcid=orcid
        
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