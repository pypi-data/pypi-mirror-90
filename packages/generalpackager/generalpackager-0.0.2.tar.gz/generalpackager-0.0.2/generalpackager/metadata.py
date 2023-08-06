

class _Metadata:
    """ Contains unaltered metadata from metadata.json. """
    name = ...
    version = ...
    description = ...
    install_requires = ...
    extras_require = ...
    topics = ...

    def __init__(self, packager):
        self.packager = packager

        for key, value in self.packager.localrepo.get_metadata_path().read().items():
            setattr(self, key, value)

        for key in dir(self):
            if getattr(self, key) is Ellipsis:
                raise AssertionError(f"Key '{key}' for {self.packager}'s metadata is still ...")

