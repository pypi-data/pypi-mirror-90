import sys
import unittest


class TestImport(unittest.TestCase):
    def setUp(self):
        pass
        

    def test_import_dataset(self):
        from pyadlml.dataset import load_act_assist
        from pyadlml.dataset import load_amsterdam
    
    def test_import_plots(self):
        from pyadlml.dataset.activities import plot