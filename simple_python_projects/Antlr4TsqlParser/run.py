import sys
import unittest
from tests.testRestApiTsqlParser import TestRestApiTsqlParser, TestClientUtils
from tests.testTsqlParser import TestTsqlParser
try:
    from coverage import coverage
    coverage_available = True
except ImportError:
    coverage_available = False


def suite():
    suite = unittest.TestSuite()
    # suite.addTest(unittest.makeSuite(TestRestApiTsqlParser))
    suite.addTest(unittest.makeSuite(TestClientUtils))
    suite.addTest(unittest.makeSuite(TestTsqlParser))
    return suite


def run():
    if coverage_available:
        cov = coverage(source=['RestApiTsqlParser', 'TsqlParser'])
        cov.start()
    result = unittest.TextTestRunner(verbosity=2).run(suite())
    if not result.wasSuccessful():
        sys.exit(1)
    if coverage_available:
        cov.stop()
        print("\nCode Coverage")
        cov.report()
    else:
        print("\nTipp:\n\tUse 'pip install coverage' to get great code "
              "coverage stats")


if __name__ == '__main__':
    run()
