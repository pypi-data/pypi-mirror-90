import unittest
from injecta.testing.servicesTester import testServices
from databricksbundle.containerInit import initContainer

class DatabricksBundleTest(unittest.TestCase):

    def test_azure(self):
        container = initContainer('test_azure')

        testServices(container)

    def test_aws(self):
        container = initContainer('test_aws')

        testServices(container)

    def test_test(self):
        container = initContainer('test_test')

        testServices(container)

if __name__ == '__main__':
    unittest.main()
