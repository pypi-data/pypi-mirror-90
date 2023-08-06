import unittest
from injecta.testing.servicesTester import testServices
from injecta.config.YamlConfigReader import YamlConfigReader
from injecta.package.pathResolver import resolvePath
from pyfonycore.Kernel import Kernel
from pyfonybundles.loader import pyfonyBundlesLoader
from consolebundle.ConsoleBundle import ConsoleBundle

class ConsoleBundleTest(unittest.TestCase):

    def test_init(self):
        bundles = [*pyfonyBundlesLoader.loadBundles(), ConsoleBundle.autodetect()]

        kernel = Kernel(
            'test',
            resolvePath('consolebundle') + '/_config',
            YamlConfigReader(),
            bundles,
        )

        container = kernel.initContainer()

        testServices(container)

if __name__ == '__main__':
    unittest.main()
