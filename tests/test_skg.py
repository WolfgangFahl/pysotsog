"""
Created on 2022-11-16

@author: wf
"""

from basemkit.basetest import Basetest

from skg.kg import SKG_Def


class TestSkg(Basetest):
    """
    test scholarly knowledge graph
    """

    def test_skg(self):
        """
        test the scholarly knowledge graph definition
        """
        skg_def = SKG_Def()
        concept = skg_def.conceptForQid("Q5")
        self.assertEqual("Scholar", concept.name)

    def test_plantuml(self):
        """
        test converting the knowledge graph definition to plantuml
        """
        skg_def = SKG_Def()
        debug = True
        plantuml = skg_def.toPlantuml()
        if debug:
            print(plantuml)
