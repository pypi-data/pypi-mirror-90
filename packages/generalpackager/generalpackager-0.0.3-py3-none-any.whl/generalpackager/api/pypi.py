

class PyPI:
    """ Tools to interface pypi.org.
        Todo: Method to upload to PyPI. """
    def __init__(self, name):
        self.name = name

        self.url = f"https://pypi.org/project/{self.name}/"
