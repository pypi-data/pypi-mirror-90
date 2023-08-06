# Detect a UTF-8-capable locale for running child processes in

Sometimes it is useful for a program to be able to run a child process and
more or less depend on its output being valid UTF-8. This can usually be
accomplished by setting one or more environment variables, but there is
the question of what to set them to - what UTF-8-capable locale is present
on this particular system? This is where the `utf8_locale` module comes in.

## Functions

### `detect_utf8_locale()`

The `detect_utf8_locale()` function runs the external `locale` command to
obtain a list of the supported locale names, and then picks a suitable one to
use so that programs are more likely to output valid UTF-8 characters and
language-neutral messages. It prefers the `C` base locale, but if neither
`C.UTF-8` nor `C.utf8` is available, it will fall back to a list of other
locale names that are likely to be present on the system.

The `utf8_locale` package has a predefined list of preferred languages.
If a program has different preferences, e.g. only expecting to parse
messages written in English, the `detect_utf8_locale()` function may be
passed a `languages` parameter - an iterable of strings - containing
the language names in the preferred order. Note that `languages` should
only contain the language name (e.g. "en") and not a territory name
(e.g. "en\_US"); locale names for the same language and different
territories are considered equivalent. Thus, the abovementioned program
that expects to parse messages in English may do:

    name = detect_utf8_locale(languages=["C", "en"])

### `get_utf8_env()`

The `get_utf8_env()` function invokes `detect_utf8_locale()` and then returns
a dictionary similar to `os.environ`, but with `LC_ALL` set to the obtained
locale name and `LANGUAGE` set to an empty string so that recent versions of
the gettext library do not choose a different language to output messages in.
If a dictionary is passed as the `env` parameter, `get_utf8_env()` uses it as
a base instead of the value of `os.environ`.

The `get_utf8_env()` function also has an optional `languages` parameter that
is passed directory to `detect_utf8_locale()`.

### `get_preferred_languages()`

The `get_preferred_languages()` function examines either the current process
environment or the provided dictionary and returns a list of the languages
specified in the locale variables (`LC_ALL`, `LANG`, `LC_MESSAGES`, etc) in
order of preference as defined by either the `names` parameter passed or
by the `LOCALE_VARIABLES` constant. It may be used by programs to add
the user's currently preferred locale to their own settings, e.g.:

    name = detect_utf8_locale(get_preferred_locales() + ["C", "en"])
