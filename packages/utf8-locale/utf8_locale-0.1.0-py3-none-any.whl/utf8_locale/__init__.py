# Copyright (c) 2020, 2021  Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

"""Detect a UTF-8-capable locale for running child processes in.

Sometimes it is useful for a program to be able to run a child process and
more or less depend on its output being valid UTF-8. This can usually be
accomplished by setting one or more environment variables, but there is
the question of what to set them to - what UTF-8-capable locale is present
on this particular system? This is where the `utf8_locale` module comes in.
"""


import os
import re
import subprocess

from typing import Dict, Iterable, List, NamedTuple, Optional  # noqa: H301

VERSION = "0.1.0"

UTF8_LANGUAGES = ("C", "en", "de", "es", "it")
UTF8_ENCODINGS = ("UTF-8", "utf8")

LOCALE_VARIABLES = (
    "LC_ALL",
    "LANG",
    "LC_MESSAGES",
    "LC_COLLATE",
    "LC_NAME",
    "LC_IDENTIFICATION",
    "LC_CTYPE",
    "LC_NUMERIC",
    "LC_TIME",
    "LC_MONETARY",
    "LC_PAPER",
    "LC_ADDRESS",
    "LC_TELEPHONE",
    "LC_MEASUREMENT",
)

RE_LOCALE_NAME = re.compile(
    r""" ^
    (?P<lang> [a-zA-Z0-9]+ )
    (?:
        _
        (?P<territory> [a-zA-Z0-9]+ )
    )?
    (?:
        \.
        (?P<codeset> [a-zA-Z0-9-]+ )
    )?
    (?:
        @
        (?P<modifier> [a-zA-Z0-9]+ )
    )?
    $ """,
    re.X,
)


class _DetectState(NamedTuple):
    """The state of processing consecutive lines of `locale -a` output."""

    priority: int
    name: str


def detect_utf8_locale(*, languages: Iterable[str] = UTF8_LANGUAGES) -> str:
    """Get a locale name that may hopefully be used for UTF-8 output.

    The `detect_utf8_locale()` function runs the external `locale` command to
    obtain a list of the supported locale names, and then picks a suitable one
    to use so that programs are more likely to output valid UTF-8 characters
    and language-neutral messages. It prefers the `C` base locale, but if
    neither `C.UTF-8` nor `C.utf8` is available, it will fall back to a list of
    other locale names that are likely to be present on the system.

    The `utf8_locale` package has a predefined list of preferred languages.
    If a program has different preferences, e.g. only expecting to parse
    messages written in English, the `detect_utf8_locale()` function may be
    passed a `languages` parameter - an iterable of strings - containing
    the language names in the preferred order. Note that `languages` should
    only contain the language name (e.g. "en") and not a territory name
    (e.g. "en_US"); locale names for the same language and different
    territories are considered equivalent. Thus, the abovementioned program
    that expects to parse messages in English may do:

        name = detect_utf8_locale(languages=["C", "en"])
    """
    weights = {}
    unweight = 0
    for lang in languages:
        if lang not in weights:
            weights[lang] = unweight
            unweight = unweight + 1
    if not weights:
        raise ValueError("No languages specified")

    state = _DetectState(unweight, "C")
    for line in subprocess.check_output(
        ["env", "LC_ALL=C", "LANGUAGE=", "locale", "-a"],
        shell=False,
        encoding="ISO-8859-1",
    ).splitlines():
        data = RE_LOCALE_NAME.match(line)
        if not data:
            raise ValueError(
                "Unexpected locale name: {line}".format(line=repr(line))
            )
        if data.group("codeset") not in UTF8_ENCODINGS:
            continue

        lang = data.group("lang")
        prio = weights.get(lang, weights.get("*", unweight))
        if prio == 0:
            return line
        if prio < state.priority:
            state = _DetectState(prio, line)

    return state.name


def get_utf8_env(
    env: Optional[Dict[str, str]] = None,
    *,
    languages: Iterable[str] = UTF8_LANGUAGES,
) -> Dict[str, str]:
    """Prepare the environment to run subprocesses in.

    The `get_utf8_env()` function invokes `detect_utf8_locale()` and then
    returns a dictionary similar to `os.environ`, but with `LC_ALL` set to
    the obtained locale name and `LANGUAGE` set to an empty string so that
    recent versions of the gettext library do not choose a different language
    to output messages in. If a dictionary is passed as the `env` parameter,
    `get_utf8_env()` uses it as a base instead of the value of `os.environ`.

    The `get_utf8_env()` function also has an optional `languages` parameter
    that is passed directory to `detect_utf8_locale()`.
    """
    utf8loc = detect_utf8_locale(languages=languages)
    subenv = dict(os.environ if env is None else env)
    subenv["LC_ALL"] = utf8loc
    subenv["LANGUAGE"] = ""
    return subenv


def get_preferred_languages(
    env: Optional[Dict[str, str]] = None,
    *,
    names: Iterable[str] = LOCALE_VARIABLES,
) -> List[str]:
    """Determine preferred languages as per the current locale settings.

    The `get_preferred_languages()` function examines either the current
    process environment or the provided dictionary and returns a list of
    the languages specified in the locale variables (`LC_ALL`, `LANG`,
    `LC_MESSAGES`, etc) in order of preference as defined by either
    the `names` parameter passed or by the `LOCALE_VARIABLES` constant.
    It may be used by programs to add the user's currently preferred locale
    to their own settings, e.g.:

        name = detect_utf8_locale(get_preferred_locales() + ["C", "en"])
    """
    if env is None:
        env = dict(os.environ)

    res = []
    for name in names:
        value = env.get(name)
        if value is None:
            continue
        data = RE_LOCALE_NAME.match(value)
        if data is None:
            continue
        if data.group("codeset") not in UTF8_ENCODINGS:
            continue

        lang = data.group("lang")
        if lang not in res:
            res.append(lang)

    return res
