Beancount Plugin Utils
===============================================================================

[![PyPI - Version](https://img.shields.io/pypi/v/beancount_plugin_utils)](https://pypi.org/project/beancount_plugin_utils/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/beancount_plugin_utils)](https://pypi.org/project/beancount_plugin_utils/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/beancount_plugin_utils)](https://pypi.org/project/beancount_plugin_utils/)
[![License](https://img.shields.io/pypi/l/beancount_plugin_utils)](https://choosealicense.com/licenses/agpl-3.0/)
[![Linting](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


A collection of utils for writing beancount plugins:
- `BeancountError` & utils - throw anywhere `RuntimeError` and have nice error output instead of crashing beancount.
- `marked` - introduce an abstraction of `mark` to liberate user to use any of: tag, tx meta, posting meta.
- `metaset` - abstraction over `meta` dict to have multiple values for the same key.
- `merge_postings` - merge postings with equal account names.
- `parse_config_string` - parse config string.

Also see test framework and feel free to copy it.

**Note: NOT READY FOR PUBLIC YET, STILL MIGRATING MY OWN PLUGINS. ANYTHING CAN CHANGE WITHOUT NOTICE.**








Install
===============================================================================

1. Add `beancount_plugin_utils` to your plugin's `requirements.txt` file or `pyproject.toml` file.
2. Reinstall your dependencies.








Tests
===============================================================================

If the examples above do not suffice your needs, check out the tests.
They consist of human-readable examples for more specific cases.








Development
===============================================================================

Please see Makefile and inline comments.

Feel free to PR your utils to add them to this repro.
