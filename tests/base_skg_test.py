'''
Created on 2022-11-21

@author: wf
'''
from tests.basetest import Basetest
from skg.kg import SKG_Def

class BaseSkgTest(Basetest):
    """
    extend the Basetest
    """
    def setUp(self, debug=False, profile=True):
        Basetest.setUp(self, debug=debug, profile=profile)
        self.skg_def=SKG_Def()
    
    def check_id_examples(self,id_examples,createFunc,checkItem,debug:bool=False):
        """
        check the given examples
        
        Args:
            id_examples(list): a list of dict with examples
            createFunct(func): a function to be  used to create items
            checkItem(func): a function to be called for testing each item
            debug(bool): if True show debug information
        """
        for id_example in id_examples:
            id_name=id_example["id_name"]
            id_value=id_example["id_value"]
            id_concept=id_example["concept"]
            # use createFunc as a factory
            items=createFunc(id_concept,id_name,id_value)
            if debug:
                for item in items:
                    print(item)
            self.assertEqual(1,len(items))
            item=items[0]
            self.assertEqual(item.concept.name,id_concept.name)
            checkItem(item,id_name,id_value,debug)