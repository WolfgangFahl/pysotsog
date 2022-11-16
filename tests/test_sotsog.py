'''
Created on 2022-11-16

@author: wf
'''
from tests.basetest import Basetest
from skg.sotsog import SotSog
class TestSotsog(Basetest):
    """
    test concerning the SotSog main class
    """

    def test_sotsog_search(self):
        """
        """
        sotsog=SotSog()
        scholars=sotsog.search(["Albert","Einstein"], lang="en", show=False, open_browser=False)
        for scholar in scholars:
            print(scholar)
