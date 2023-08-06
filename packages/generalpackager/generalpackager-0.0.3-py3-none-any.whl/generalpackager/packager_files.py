
from generallibrary import CodeLine, current_datetime
from generalfile import Path


class _PackagerFiles:
    """ Generates setup, license and gitexclude. """
    def generate_file(self, path, text):
        """ Overwrite a file in local repo with generated text.

            :param generalpackager.Packager self:
            :param path:
            :param text: """
        path.text.write(text, overwrite=True)

    def generate_setup(self):
        """ Generate setup.py and overwrite local repo.

            :param generalpackager.Packager self: """
        setup_kwargs = {
            "name": f'"{self.metadata.name}"',
            "author": f"'{self.author}'",
            "author_email": f'"{self.email}"',
            "version": f'"{self.metadata.version}"',
            "description": f'"{self.metadata.description}"',
            "long_description": f"Path(r'{self.localrepo.get_readme_path()}').read_text(encoding='utf-8')",
            "long_description_content_type": '"text/markdown"',
            "install_requires": self.metadata.install_requires,
            "url": f'"{self.github.url()}"',
            "license": f'"{self.license}"',
            "python_requires": f'"{", ".join([f"=={ver}.*" for ver in self.python])}"',
            "packages": 'find_namespace_packages(exclude=("build*", "dist*"))',
            "extras_require": self.metadata.extras_require,
            "classifiers": self.get_classifiers(),
        }

        top = CodeLine()
        top.add(CodeLine("from setuptools import setup, find_namespace_packages", space_before=1))
        top.add(CodeLine("from pathlib import Path", space_after=1))

        setup = top.add(CodeLine("setup("))
        for key, value in setup_kwargs.items():
            if isinstance(value, list):
                list_ = setup.add(CodeLine(f"{key}=["))
                for item in value:
                    list_.add(CodeLine(f"'{item}',"))
                setup.add(CodeLine("],"))
            else:
                setup.add(CodeLine(f"{key}={value},"))

        top.add(CodeLine(")", space_after=1))

        self.generate_file(self.localrepo.get_setup_path(), top.text(watermark=False))

    def generate_git_exclude(self):
        """ Generate git exclude file.

            :param generalpackager.Packager self: """
        self.generate_file(self.localrepo.get_git_exclude_path(), "\n".join(self.git_exclude_lines))

    def generate_license(self):
        """ Generate LICENSE by using Packager.license.

            :param generalpackager.Packager self: """
        text = Path(self.repos_path / f"generalpackager/generalpackager/licenses/{self.license}").text.read()
        assert "$" in text
        text = text.replace("$year", str(current_datetime().year))
        text = text.replace("$author", self.author)
        assert "$" not in text

        self.generate_file(self.localrepo.get_license_path(), text)
