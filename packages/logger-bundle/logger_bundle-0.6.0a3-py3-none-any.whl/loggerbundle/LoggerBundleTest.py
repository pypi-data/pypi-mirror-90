import unittest
from injecta.testing.servicesTester import testServices
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.package.pathResolver import resolvePath
from pyfonycore.Kernel import Kernel
from pyfonybundles.loader import pyfonyBundlesLoader
from loggerbundle.LoggerBundle import LoggerBundle

class LoggerBundleTest(unittest.TestCase):

    def test_init(self):
        bundles = [*pyfonyBundlesLoader.loadBundles(), LoggerBundle.autodetect()]

        kernel = Kernel(
            'test',
            resolvePath('loggerbundle') + '/_config',
            YamlConfigReader(),
            bundles,
        )

        container = kernel.initContainer()

        testServices(container)

if __name__ == '__main__':
    unittest.main()
