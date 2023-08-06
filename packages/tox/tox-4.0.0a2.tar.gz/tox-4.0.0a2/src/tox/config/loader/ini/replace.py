"""
Apply value substitution (replacement) on tox strings.
"""
import os
import re
import sys
from configparser import SectionProxy
from typing import TYPE_CHECKING, Iterator, List, Optional, Sequence, Tuple, Union

from tox.config.loader.stringify import stringify
from tox.config.main import Config
from tox.config.sets import ConfigSet
from tox.execute.request import shell_cmd

if TYPE_CHECKING:
    from tox.config.loader.ini import IniLoader

CORE_PREFIX = "tox"
BASE_TEST_ENV = "testenv"

ARGS_GROUP = re.compile(r"(?<!\\):")


def replace(value: str, conf: Config, name: Optional[str], loader: "IniLoader") -> str:
    # perform all non-escaped replaces
    start, end = 0, 0
    while True:
        start, end, match = _find_replace_part(value, start, end)
        if not match:
            break
        to_replace = value[start + 1 : end]
        replaced = _replace_match(conf, name, loader, to_replace)
        if replaced is None:
            # if we cannot replace, keep what was there, and continue looking for additional replaces following
            # note, here we cannot raise because the content may be a factorial expression, and in those case we don't
            # want to enforce escaping curly braces, e.g. it should work to write: env_list = {py39,py38}-{,dep}
            start = end = end + 1
            continue
        new_value = value[:start] + replaced + value[end + 1 :]
        start, end = 0, 0  # if we performed a replace start over
        if new_value == value:  # if we're not making progress stop (circular reference?)
            break
        value = new_value
    # remove escape sequences
    value = value.replace("\\{", "{")
    value = value.replace("\\}", "}")
    return value


def _find_replace_part(value: str, start: int, end: int) -> Tuple[int, int, bool]:
    match = False
    while end != -1:
        end = value.find("}", end)
        if end == -1:
            continue
        if end >= 1 and value[end - 1] == "\\":  # ignore escaped
            end += 1
            continue
        before = end
        while True:
            start = value.rfind("{", 0, before)
            if start >= 1 and value[start - 1] == "\\":  # ignore escaped
                before = start - 1
                continue
            match = start != -1
            break
        break  # pragma: no cover # for some odd reason this line is not reported by coverage, though is needed
    return start, end, match


def _replace_match(conf: Config, current_env: Optional[str], loader: "IniLoader", value: str) -> Optional[str]:
    of_type, *args = ARGS_GROUP.split(value)
    if of_type == "env":
        replace_value: Optional[str] = replace_env(args)
    elif of_type == "tty":
        replace_value = replace_tty(args)
    elif of_type == "posargs":
        replace_value = replace_pos_args(args, conf.pos_args)
    else:
        replace_value = replace_reference(conf, current_env, loader, value)
    return replace_value


_REPLACE_REF = re.compile(
    rf"""
    (\[(?P<full_env>{BASE_TEST_ENV}(:(?P<env>[^]]+))?|(?P<section>\w+))\])? # env/section
    (?P<key>[a-zA-Z0-9_]+) # key
    (:(?P<default>.*))? # default value
""",
    re.VERBOSE,
)


def replace_reference(
    conf: Config,
    current_env: Optional[str],
    loader: "IniLoader",
    value: str,
) -> Optional[str]:
    # a return value of None indicates could not replace
    match = _REPLACE_REF.match(value)
    if match:
        settings = match.groupdict()

        key = settings["key"]
        if settings["section"] is None and settings["full_env"] == BASE_TEST_ENV:
            settings["section"] = BASE_TEST_ENV

        exception: Optional[Exception] = None
        try:
            for src in _config_value_sources(settings["env"], settings["section"], current_env, conf, loader):
                try:
                    if isinstance(src, SectionProxy):
                        return src[key]
                    value = src[key]
                    as_str, _ = stringify(value)
                    return as_str
                except KeyError as exc:  # if fails, keep trying maybe another source can satisfy
                    exception = exc
        except Exception as exc:
            exception = exc
        if exception is not None:
            if isinstance(exception, KeyError):  # if the lookup failed replace - else keep
                default = settings["default"]
                if default is not None:
                    return default
                # we cannot raise here as that would mean users could not write factorials: depends = {py39,py38}-{,b}
            else:
                raise exception
    return None


def _config_value_sources(
    env: Optional[str],
    section: Optional[str],
    current_env: Optional[str],
    conf: Config,
    loader: "IniLoader",
) -> Iterator[Union[SectionProxy, ConfigSet]]:
    # if we have an env name specified take only from there
    # config is None only when loading the global tox config file for the CLI arguments, in this case no replace works
    if env is not None:
        if env in conf:
            yield conf.get_env(env)
        else:
            raise KeyError(f"missing tox environment with name {env}")

    # if we have a section name specified take only from there
    if section is not None:
        # special handle the core section under name tox
        if section == CORE_PREFIX:
            yield conf.core  # try via registered configs
        value = loader.get_section(section)  # fallback to section
        if value is not None:
            yield value
        return

    # otherwise try first from core conf, and fallback to our own environment
    yield conf.core
    if current_env is not None:
        yield conf.get_env(current_env)


def replace_pos_args(args: List[str], pos_args: Optional[Sequence[str]]) -> str:
    if pos_args is None:
        if args:
            replace_value = ":".join(args)  # if we use the defaults join back remaining args
        else:
            replace_value = ""
    else:
        replace_value = shell_cmd(pos_args)
    return replace_value


def replace_env(args: List[str]) -> str:
    key = args[0]
    default = "" if len(args) == 1 else args[1]
    return os.environ.get(key, default)


def replace_tty(args: List[str]) -> str:
    if sys.stdout.isatty():
        result = args[0] if len(args) > 0 else ""
    else:
        result = args[1] if len(args) > 1 else ""
    return result


__all__ = (
    "CORE_PREFIX",
    "BASE_TEST_ENV",
    "replace",
)
