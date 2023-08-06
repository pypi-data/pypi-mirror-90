import sys
import subprocess
import toml


class PyScript:

    _config = None

    @property
    def config(self) -> dict:
        if self._config is None:
            self._config = toml.load("pyproject.toml")["tool"]["pyscript"]
        return self._config

    def run(self):
        script_name = sys.argv[1]
        script_import_path = self.config[script_name]
        module, _callable = script_import_path.split(":")
        result = subprocess.run(
            [
                "/usr/bin/env",
                "python",
                "-c",
                "import sys;"
                "from importlib import import_module;"
                f"sys.argv = {sys.argv[1:]};"
                f"import_module('{module}').{_callable}()",
            ]
        )
        return sys.exit(result.returncode)


def main():
    pyscript = PyScript()
    pyscript.run()
