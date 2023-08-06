
import unittest
import os

from generalpackager.test.test_github import TestGitHub


def run_tests(token=None):
    """ Run all unittests. """
    if token is not None:
        os.environ['packager_github_api'] = token

    runner = unittest.TextTestRunner()
    itersuite = unittest.TestLoader().loadTestsFromTestCase(TestGitHub)
    runner.run(itersuite)


# if __name__ == "__main__":
#     run_tests()
