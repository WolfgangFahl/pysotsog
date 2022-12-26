'''
Created on 2022-11-22

@author: wf
'''
import datetime

class Schema():
    """
    a schema
    """
    
    def __init__(self,name:str,url:str,authors:str,inception:str):
        """
        constructor
            
        Args:
            name(str): the name of this schema
            url(str): the url of this schema
            authors(str): the authors of this schema
            inception(str): the inception of this schema
        """
        self.name=name
        self.url=url
        self.authors=authors
        self.inception=inception
        
    def classesToPlantUml(self,classes:dict,indent:str="  "):
        """
        convert the given classes dict to plantuml
        
        Args:
            classes(dict): a dictionary of classes
            indent(str): the indentation to apply
        """
        classes=classes["classes"]
        markup=""
        for cname,clazz in classes.items():
            class_markup=""
            rel_markup="" # relations
            for pname,prop in clazz.items():
                if pname.startswith("@"):
                    pass
                else:
                    prange=prop['range']
                    if prange in classes:
                        #  Class01 "1" *-- "many" Class02 : contains
                        rel_markup+=f"{indent}{cname}--{prange}:{pname}\n"
                    else:
                        class_markup+=f"{indent}  {pname}:{prange}\n"
            class_markup=f"{indent}class {cname}{{\n{class_markup}\n{indent}}}\n"
            class_markup+=rel_markup
            if "@subClassOf" in clazz:
                general=clazz["@subClassOf"]
                if general:
                    class_markup+=f"{indent}{general} <|-- {cname}\n"
            note=f"{indent}note top of {cname}\n"
            if "@label" in clazz:
                note+=f"""{indent}{clazz["@label"]}\n"""
            if "@comment" in clazz:
                note+=f"""{indent}{clazz["@comment"]}\n"""
            note+=f"{indent}end note\n"
            class_markup=note+class_markup
            markup+=class_markup
        return markup
        
    def toPlantUml(self,header=None,footer=None)->str:
            """
            get a plantuml version of the schema
            
            Args:
                header(str): the header to apply
                footer(str): the footer to apply
            
            Returns:
                str: the plantuml markup
            """
            timestamp=datetime.datetime.utcnow().strftime('%Y-%m-%d')
            if header is None:
                header=f"""/'
     {self.authors} {self.inception}
     updated {timestamp}
      
     {self.name} {self.schema_url}
     converted from owl to plantuml
    '/
    title  {self.name} schema {self.schema_url} converted from owl to plantuml updated {timestamp}
    hide circle
    package foaf {{
      class Document {{
      }}
    }}
    package dblp {{
     """
            if footer is None:
                footer="}\n"
            classes=self.toClasses()
            markup=header+self.classesToPlantUml(classes,indent="  ")+footer
            return markup