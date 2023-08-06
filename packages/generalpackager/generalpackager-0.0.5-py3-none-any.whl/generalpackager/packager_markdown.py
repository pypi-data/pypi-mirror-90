
from generallibrary import Markdown, comma_and_and, current_datetime_formatted


class _PackagerMarkdown:
    """ Contains methods to generate readme sections from arguments.
        Todo: Inherit future crawler class for pypi and github.
        Todo: Use Packager.os for badges. """
    def get_badges_dict(self):
        """ Get badges as a dict.

            :param generalpackager.Packager self: """
        badges = {
            "UnitTests": "[![workflow Actions Status](https://github.com/ManderaGeneral/PACKAGE/workflows/workflow/badge.svg)](https://github.com/ManderaGeneral/PACKAGE/actions)",
            "Commit": "![GitHub last commit](https://img.shields.io/github/last-commit/ManderaGeneral/PACKAGE)",
            "Release": "[![PyPI version shields.io](https://img.shields.io/pypi/v/PACKAGE.svg)](https://pypi.org/project/PACKAGE/)",
            "Python": "[![PyPI pyversions](https://img.shields.io/pypi/pyversions/PACKAGE.svg)](https://pypi.python.org/pypi/PACKAGE/)",
            "Operating System": "[![Generic badge](https://img.shields.io/badge/platforms-Windows%20%7C%20Ubuntu%20%7C%20MacOS-blue.svg)](https://shields.io/)",
        }
        return {key: value.replace("PACKAGE", self.name) for key, value in badges.items()}

    def get_installation_markdown(self):
        """ Get install markdown.

            :param generalpackager.Packager self: """
        markdown = Markdown(header="Installation").add_code_lines(f'pip install {self.name}')

        if len(self.localrepo.extras_require) > 1:
            list_of_dicts = [{
                "Name": extra,
                "Command": f"`pip install {self.name}[{extra}]`",
                "Extra packages": comma_and_and(*[f"`{x}`" for x in requires], period=False),
            } for extra, requires in self.localrepo.extras_require.items()]

            Markdown(header="Extras", parent=markdown).add_table_lines(*list_of_dicts)

        return markdown

    def configure_contents_markdown(self, markdown):
        """ Configure table of contents lines from markdown.

            :param generalpackager.Packager self:
            :param markdown: """
        parent_markdown = markdown.get_parent(-1)
        markdown.add_pre_lines(parent_markdown.view(custom_repr=lambda md: md.link(md.header, href=True), print_out=False))
        return markdown

    def _attr_repr(self, objInfo):
        """ Return a nice representation of each attribute made by this module, in this case a link to code definition.

            :param generalpackager.Packager self:
            :param generallibrary.ObjInfo objInfo: """
        text = objInfo.nice_repr()
        commit_sha = self.commit_sha
        file_path = f'{objInfo.module().__name__.replace(".", "/")}{"/__init__" if objInfo.is_module() else ""}.py'
        line = objInfo.get_definition_line()

        return self.github_link(text=text, suffix=f"blob/{commit_sha}/{file_path}#L{line}")

    def github_link(self, text, suffix):
        """ :param generalpackager.Packager self:
            :param text:
            :param suffix: """
        url = f"{self.github.url()}/{suffix}"
        # self.assert_url_up(url=url)  # Wont work for private repos or new files, would have to check after the fact.
        return Markdown.link(text=text, url=url, href=True)

    def get_attributes_markdown(self):
        """ Get a recursive view of attributes markdown.

            :param generalpackager.Packager self: """
        view_str = self.localmodule.objInfo.view(custom_repr=self._attr_repr, print_out=False)
        return Markdown(header="Attributes").add_pre_lines(view_str)

    def get_footnote_markdown(self):
        """ Get a markdown for footnote containing date, time and commit link.

            :param generalpackager.Packager self: """
        line = f"Generated {current_datetime_formatted()} for commit {self.github_link(text=self.commit_sha, suffix=f'commit/{self.commit_sha}')}."
        return Markdown(line).wrap_with_tags("sup")


    def generate_readme(self):
        """ Generate readme markdown and overwrite README.md in local repo.

            :param generalpackager.Packager self: """
        # Description
        markdown = Markdown(self.localrepo.description, header=self.name)

        # Badges
        markdown.add_lines(*self.get_badges_dict().values())

        # Table of contents - Placeholder
        contents = Markdown(header="Contents", parent=markdown)

        # Installation
        self.get_installation_markdown().set_parent(parent=markdown)

        # Attributes
        self.get_attributes_markdown().set_parent(parent=markdown)

        # Todos
        Markdown(header="Todos", parent=markdown).add_table_lines(*self.localrepo.get_todos())

        # Table of contents - Configuration
        self.configure_contents_markdown(markdown=contents)

        # Footnote
        self.get_footnote_markdown().set_parent(parent=markdown)

        # Create actual readme file
        self.generate_file(self.localrepo.get_readme_path(), markdown)
