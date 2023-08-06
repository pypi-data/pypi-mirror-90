
from generallibrary import CodeLine


class _PackagerWorkflow:
    @staticmethod
    def _var(string):
        return f"${{{{ {string} }}}}"

    @staticmethod
    def _contains(haystack, needle):
        return f"contains({haystack}, {needle})"

    _commit_message = "github.event.head_commit.message"
    _skip_str = "'[CI SKIP]'"
    _action_checkout = "actions/checkout@v2"
    _action_setup_python = "actions/setup-python@v2"
    _matrix_os = "matrix.os"
    _matrix_python_version = "matrix.python-version"

    def __init__(self):
        self._secrets_token = self._var('secrets.ACTIONS_TOKEN')

    def get_triggers(self):
        """ :param generalpackager.Packager self: """
        on = CodeLine("on:")
        push = on.add("push:")
        branches = push.add("branches:")
        branches.add("- master")
        return on

    def get_step(self, name, *codelines):
        """ . """
        step = CodeLine(f"- name: {name}")
        for codeline in codelines:
            step.add(codeline)
        return step

    def step_checkout(self):
        """ :param generalpackager.Packager self: """
        return self.get_step("Checkout repository.", "uses: actions/checkout@v2")

    def step_setup_python(self, version):
        """ :param generalpackager.Packager self:
            :param version: """
        with_ = CodeLine("with:")
        with_.add(f"python-version: {version}")
        return self.get_step(f"Setting up python version '{version}'.", f"uses: {self._action_setup_python}", with_)

    def step_install_package(self):
        """ :param generalpackager.Packager self: """
        run = CodeLine("run: |")
        run.add("python -m pip install --upgrade pip")
        run.add("pip install wheel")
        run.add("pip install .[full]")
        return self.get_step(f"Install package '{self.name}'.", run)

    def step_run_unittests(self):
        """ :param generalpackager.Packager self: """
        run = CodeLine("run: |")
        # run.add(f"python -m unittest discover {self.name}/test")
        run.add(f"python -c \"from generalpackager.test.main import run_tests; run_tests('{self._secrets_token}')\"")
        return self.get_step(f"Run unittests.", run)



    def get_unittest_job(self):
        """ :param generalpackager.Packager self: """
        unittest = CodeLine("unittest:")
        unittest.add(f"if: !{self._contains(self._commit_message, self._skip_str)}")
        unittest.add(f"runs-on: {self._var(self._matrix_os)}")

        strategy = unittest.add("strategy:")
        matrix = strategy.add("matrix:")
        matrix.add(f"python-version: {list(self.python)}".replace("'", ""))
        matrix.add(f"os: {[f'{os}-latest' for os in self.os]}".replace("'", ""))

        steps = unittest.add("steps:")
        steps.add(self.step_checkout())
        steps.add(self.step_setup_python(version=self._var(self._matrix_python_version)))
        steps.add(self.step_install_package())
        steps.add(self.step_run_unittests())

        return unittest





