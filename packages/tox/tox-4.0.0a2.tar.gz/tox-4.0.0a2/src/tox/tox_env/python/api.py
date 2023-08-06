"""
Declare the abstract base class for tox environments that handle the Python language.
"""
import logging
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, NamedTuple, Optional, Sequence, Union, cast

from packaging.requirements import Requirement
from virtualenv.discovery.py_spec import PythonSpec

from tox.config.cli.parser import Parsed
from tox.config.main import Config
from tox.config.sets import ConfigSet
from tox.journal import EnvJournal
from tox.report import ToxHandler
from tox.tox_env.api import ToxEnv
from tox.tox_env.errors import Fail, Recreate, Skip


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int


class PythonInfo(NamedTuple):
    executable: Path
    implementation: str
    version_info: VersionInfo
    version: str
    is_64: bool
    platform: str
    extra_version_info: Optional[str]


class PythonDep:
    def __init__(self, value: Union[Path, Requirement]) -> None:
        self._value = value

    @property
    def value(self) -> Union[Path, Requirement]:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other: Any) -> bool:
        return type(self) == type(other) and str(self) == str(other)

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value!r})"


PythonDeps = Sequence[PythonDep]


class Python(ToxEnv, ABC):
    def __init__(
        self, conf: ConfigSet, core: ConfigSet, options: Parsed, journal: EnvJournal, log_handler: ToxHandler
    ) -> None:
        self._base_python: Optional[PythonInfo] = None
        self._base_python_searched: bool = False
        super().__init__(conf, core, options, journal, log_handler)

    def register_config(self) -> None:
        super().register_config()
        self.conf.add_config(
            keys=["base_python", "basepython"],
            of_type=List[str],
            default=self.default_base_python,
            desc="environment identifier for python, first one found wins",
        )
        self.conf.add_constant(
            keys=["env_site_packages_dir", "envsitepackagesdir"],
            desc="the python environments site package",
            value=lambda: self.env_site_package_dir(),
        )
        self.conf.add_constant(
            ["env_python", "envpython"],
            desc="python executable from within the tox environment",
            value=lambda: self.env_python(),
        )

    def default_pass_env(self) -> List[str]:
        env = super().default_pass_env()
        if sys.platform == "win32":  # pragma: win32 cover
            env.extend(
                [
                    "SYSTEMROOT",  # needed for python's crypto module
                    "PATHEXT",  # needed for discovering executables
                    "COMSPEC",  # needed for distutils cygwin compiler
                    "PROCESSOR_ARCHITECTURE",  # platform.machine()
                    "USERPROFILE",  # needed for `os.path.expanduser()`
                    "MSYSTEM",  # controls paths printed format
                ]
            )
        return env

    def default_base_python(self, conf: "Config", env_name: Optional[str]) -> List[str]:
        spec = PythonSpec.from_string_spec(env_name)
        if spec.implementation is not None:
            if spec.implementation.lower() in ("cpython", "pypy") and env_name is not None:
                return [env_name]
        return [sys.executable]

    @abstractmethod
    def env_site_package_dir(self) -> Path:
        """
        If we have the python we just need to look at the last path under prefix.
        E.g., Debian derivatives change the site-packages to dist-packages, so we need to fix it for site-packages.
        """
        raise NotImplementedError

    @abstractmethod
    def env_python(self) -> Path:
        """The python executable within the tox environment"""
        raise NotImplementedError

    def setup(self) -> None:
        """setup a virtual python environment"""
        conf = self.python_cache()
        with self._cache.compare(conf, Python.__name__) as (eq, old):
            if eq is False:  # if changed create
                self.create_python_env()
            self._paths = self.paths()
        super().setup()

    def setup_has_been_done(self) -> None:
        """called when setup is done"""
        super().setup_has_been_done()
        if self.journal:
            outcome = self.get_installed_packages()
            self.journal["installed_packages"] = outcome

    @abstractmethod
    def get_installed_packages(self) -> List[str]:
        raise NotImplementedError

    def python_cache(self) -> Dict[str, Any]:
        return {
            "version_info": list(self.base_python.version_info),
            "executable": str(self.base_python.executable),
        }

    @property
    def base_python(self) -> PythonInfo:
        """Resolve base python"""
        if self._base_python_searched is False:
            base_pythons = self.conf["base_python"]
            self._base_python_searched = True
            self._base_python = self._get_python(base_pythons)
            if self._base_python is None:
                if self.core["skip_missing_interpreters"]:
                    raise Skip
                raise NoInterpreter(base_pythons)
            if self.journal:
                value = {
                    "executable": str(self._base_python.executable),
                    "implementation": self._base_python.implementation,
                    "version_info": tuple(self.base_python.version_info),
                    "version": self._base_python.version,
                    "is_64": self._base_python.is_64,
                    "sysplatform": self._base_python.platform,
                    "extra_version_info": None,
                }
                self.journal["python"] = value
        return cast(PythonInfo, self._base_python)

    @abstractmethod
    def _get_python(self, base_python: List[str]) -> Optional[PythonInfo]:
        raise NotImplementedError

    def cached_install(self, deps: PythonDeps, section: str, of_type: str) -> bool:
        conf_deps: List[str] = [str(i) for i in deps]
        with self._cache.compare(conf_deps, section, of_type) as (eq, old):
            if eq is True:
                return True
            if old is None:
                old = []
            missing = [PythonDep(Requirement(i)) for i in (set(old) - set(conf_deps))]
            if missing:  # no way yet to know what to uninstall here (transitive dependencies?)
                # bail out and force recreate
                logging.warning(f"recreate env because dependencies removed: {', '.join(str(i) for i in missing)}")
                raise Recreate
            new_deps_str = set(conf_deps) - set(old)
            new_deps = [PythonDep(Requirement(i)) for i in new_deps_str]
            self.install_python_packages(packages=new_deps, of_type=of_type)
        return False

    @abstractmethod
    def create_python_env(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def paths(self) -> List[Path]:
        raise NotImplementedError

    @abstractmethod
    def install_python_packages(self, packages: PythonDeps, of_type: str, no_deps: bool = False) -> None:
        raise NotImplementedError


class NoInterpreter(Fail):
    """could not find interpreter"""

    def __init__(self, base_pythons: List[str]) -> None:
        self.base_pythons = base_pythons

    def __str__(self) -> str:
        return f"could not find python interpreter matching any of the specs {', '.join(self.base_pythons)}"
