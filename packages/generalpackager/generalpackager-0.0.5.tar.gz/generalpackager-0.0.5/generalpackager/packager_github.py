

class _PackagerGitHub:
    """ Sync metadata. """
    def sync_github_metadata(self):
        """ Sync GitHub with local metadata.

            :param generalpackager.Packager self: """
        self.github.set_website(self.pypi.url)
        self.github.set_description(self.localrepo.description)
        self.github.set_topics(*self.get_topics())

