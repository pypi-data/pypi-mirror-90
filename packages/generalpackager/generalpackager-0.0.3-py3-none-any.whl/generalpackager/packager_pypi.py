
import subprocess


class _PackagerPypi:
    def create_sdist(self):
        """ Create source distribution.

            :param generalpackager.Packager self: """
        subprocess.call("python -m pip install --upgrade pip")
        subprocess.call("python -m pip install setuptools wheel")
        subprocess.call("python setup.py sdist bdist_wheel")

    def upload(self):
        """ Upload local repo to PyPI.

            :param generalpackager.Packager self: """
        self.create_sdist()
        subprocess.call("twine upload dist/* --skip-existing")

