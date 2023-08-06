import importlib
import inspect
import os
import sys
from functools import partial
from importlib._bootstrap_external import _NamespaceLoader
from types import ModuleType
from typing import List, Optional

from setuptools import find_packages, setup
from sphinx.setup_command import BuildDoc

from distutils.cmd import Command  # isort:skip

# desker metadata ---------------------------------------------------------- #
name = "desker"
version = "1.0a0"
release = "1.0"
# -------------------------------------------------------------------------- #

here = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, here)


class PrepareSphinxCmd(Command):
    """A custom command to generate .rst doc files.
    """

    description = 'Create .rst files from desker modules'
    user_options = [
        # The format is (long option, short option, description).
        ('project', 'p', 'project name (name of the base package)'),
        ('output', 'o', 'folder to store .rst files'),
    ]

    def initialize_options(self):
        """Set default values for options."""
        # Each user option must be listed here with their default value.
        self.output = 'docs/'
        self.project = "desker"

    def finalize_options(self):
        """Post-process options."""
        assert os.path.exists(self.output), (
            f'Output directory {self.output} does not exist.')

    def __recursive_import(self, module_name: str) -> ModuleType:
        """Load a module and all its submodule

        Returns
        -------
        ModuleType
            The root module (given by module_name)
        """

        try:
            module = importlib.import_module(module_name, package=self.project)
        except ModuleNotFoundError as err:
            self.__error(f"Error while importing {module_name}: {err}")
            return

        if isinstance(module.__loader__, _NamespaceLoader):
            # this is not a module but just a namespace
            return

        for f in module.__loader__.contents():
            if ('__' in f) or ('.' in f):
                continue
            self.__recursive_import(f"{module_name}.{f}")
        return module

    def __is_submodule(self, m: object, loc: str) -> bool:
        """Detect if the given object is module stored in
        the given loc.

        Parameters
        ----------
        m : object
            Python object
        loc : str
            base directory where the module should live
        """
        return inspect.ismodule(m) and hasattr(
            m, "__path__") and m.__path__[0].startswith(loc)

    def __recursive_build_doc_module(
            self,
            module: ModuleType) -> List[str]:
        """Create .rst files from given module and store
        them into the output folder

        Returns
        -------
        List[str]
            List of all the submodules (they must be added to
            the table of content for instance)
        """
        # output folder
        folder = os.path.abspath(self.output)

        # filter submodules
        loc = os.path.dirname(module.__loader__.path)
        select = partial(self.__is_submodule, loc=loc)
        submodules = inspect.getmembers(module,
                                        predicate=select)
        out: List[str] = []
        for _, m in submodules:
            # ignore built-in modules
            if inspect.isbuiltin(module):
                continue
            # only consider submodules with "public API" (__all__ well defined)
            if hasattr(m, '__all__'):
                target = os.path.join(folder, f"{m.__name__}.rst")
                # write file
                self.__log(f"Creating file {target}")
                with open(target, 'w') as w:
                    title = f"{m.__name__} module"
                    header = "=" * len(title)
                    w.write(f"{title}\n{header}\n\n")
                    w.write(f"Functions\n---------\n\n")
                    w.write(f".. automodule:: {m.__name__}\n")
                    w.write("\t:members:\n")
                    w.write("\t:undoc-members:\n")
                    # w.write('\n')

                out.append(f"{m.__name__}")
            else:
                out += self.__recursive_build_doc_module(m)
        return out

    def __build_index(
            self,
            toc: List[str],
            title: Optional[str] = None) -> None:
        """Create index.rst file
        """
        if title is None:
            title = f"{self.project} documentation"

        with open(os.path.join(self.output, "index.rst"), "w") as w:
            w.write(title + '\n')
            w.write('*' * len(title) + '\n\n')
            w.write(".. toctree::\n")
            w.write("\t:maxdepth: 2\n")
            w.write("\t:caption: Contents:\n")
            w.write("\n")
            w.write("\t" + "\n\t".join(toc) + "\n")

    def __log(self, msg: str, bold: bool = False, **kwargs):
        if bold:
            print(f"\033[1m{msg}\033[0m", **kwargs)
        else:
            print(f"{msg}", **kwargs)

    def __error(self, msg: str, **kwargs):
        print(f"\033[91m{msg}\033[0m", **kwargs)

    def __warn(self, msg: str, **kwargs):
        print(f"\033[93m{msg}\033[0m", **kwargs)

    def run(self):
        """Run command."""
        print(sys.path)
        # loads all the package
        self.__log(f"Importing {self.project}...", bold=True, end=' ')
        root_module = self.__recursive_import(self.project)
        print(list(root_module.__loader__.contents()))
        self.__log("done")
        # create the .rst files and return the corresponding modules
        self.__log("Creating documentation files", bold=True)
        index = self.__recursive_build_doc_module(root_module)
        self.__log("done")
        # create the index.rest file
        self.__log("Creating index...", bold=True, end=' ')
        self.__build_index(index)
        self.__log("done")


setup(
    name=name,
    version=version,
    description="DESKtop Elements Recognition",
    packages=find_packages(),
    include_package_data=False,
    author=["jpd", "asr", "ljk", "fgy"],
    author_email="contact@amossys.fr",
    url="https://gitlab.com/d3sker/desker",
    package_data={
        # include models
        "desker.login.knn": ["*.knn"],
        "desker.login.cnn": ["*.cnn"],
        "desker.faster_rcnn": ["labels.json"],
        "desker.nlp.pipotron": ["templates/*.yml"],
    },
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    install_requires=open("requirements.txt").read().splitlines(),
    # sphinx docs
    cmdclass={'build_sphinx': BuildDoc,
              'prepare_sphinx': PrepareSphinxCmd},
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'docs'),
            'build_dir': ('setup.py', 'docs/build')
        },
        'prepare_sphinx': {
            "project": ('setup.py', name),
            "output": ('setup.py', 'docs'),
        }
    },
)
