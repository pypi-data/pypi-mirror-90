from collections import namedtuple
from typing import NamedTuple, List
from beancount.parser import printer
from contextlib import contextmanager
from beancount.core.data import Directive, Entries, Posting, Transaction, new_metadata
import sys, traceback
import os

BeancountErrorNamedTuple = namedtuple("BeancountError", "source message entry")


class BeancountError(RuntimeError):
    def __init__(self, source, message, entry, named_tuple=BeancountErrorNamedTuple):
        self.source = source
        self.message = message
        self.entry = entry
        self.named_tuple = named_tuple

    def __str__(self):
        return printer.format_error(self.to_named_tuple())

    def to_named_tuple(self):
        return self.named_tuple(self.source, self.message, self.entry)


@contextmanager
def plugin_error_handler(
    entries: Entries,
    new_entries: Entries,
    errors: List[NamedTuple],
    name: str,
    named_tuple: NamedTuple = BeancountErrorNamedTuple,
):
    """
    Packages plugin-level errors for nice display within beancount.

    Usage:
        new_entries: Entries = []
        errors: List[NamedTuple] = []

        with plugin_error_handler(entries, new_entries, errors, "example_plugin", PluginExampleError):
            raise RuntimeError('Hello World!')

        return new_entries, errors

    Args:
        entry [Directive]: current entry.
        new_entries [Entries]: list where to push original entry in case of error.
        errors [List[NamedTuple]]: list where to push the error.
        named_tuple [NamedTuple] (optional): use plugin-specific tuple instead of generic one.
    """
    try:
        yield
    except BeancountError as e:
        new_entries[:] = entries
        errors[:] = [e.to_named_tuple()]
    except Exception as e:
        if "PYTEST_CURRENT_TEST" in os.environ:
            print("\n")
            print("Stack trace (pytest environment only):")
            print("------------------------------------------------")
            traceback.print_exc(file=sys.stdout)
            print("\n")
        new_entries[:] = entries
        errors[:] = [named_tuple(new_metadata("<" + name + ">", 0), str(e), None)]


@contextmanager
def entry_error_handler(
    entry: Directive, new_entries: Entries, errors: List[NamedTuple], named_tuple: NamedTuple = BeancountErrorNamedTuple
):
    """
    Packages entry-level errors for nice display within beancount.

    Usage:
        for entry in entries:
            with entry_error_handler(entry, new_entries, errors):
                raise RuntimeError('Hello World!')

    Args:
        entry [Directive]: current entry.
        new_entries [Entries]: list where to push original entry in case of error.
        errors [List[NamedTuple]]: list where to push the error.
        named_tuple [NamedTuple] (optional): use plugin-specific tuple instead of generic one.
    """
    try:
        yield
    except BeancountError as e:
        new_entries.append(entry)
        errors.append(e.to_named_tuple())
    except Exception as e:
        if "PYTEST_CURRENT_TEST" in os.environ:
            print("\n")
            print("Stack trace (pytest environment only):")
            print("------------------------------------------------")
            traceback.print_exc(file=sys.stdout)
            print("\n")
        new_entries.append(entry)
        errors.append(named_tuple(entry.meta, str(e), entry))


@contextmanager
def posting_error_handler(tx_orig: Transaction, posting: Posting, named_tuple=BeancountErrorNamedTuple):
    """
    Packages posting-level errors for nice display within beancount.

    Usage:
        for entry in entries:
            for posting in entry.postings:
                with posting_error_handler(entry, posting, PluginExampleError):
                    raise RuntimeError('Hello World!')

    Args:
        tx_orig [Transaction]: the Transaction this posting is from.
        posting [Entries]: current posting.
        named_tuple [NamedTuple] (optional): use plugin-specific tuple instead of generic one.
    """
    try:
        yield
    except BeancountError as e:
        raise e
    except Exception as e:
        if "PYTEST_CURRENT_TEST" in os.environ:
            print("\n")
            print("Stack trace (pytest environment only):")
            print("------------------------------------------------")
            traceback.print_exc(file=sys.stdout)
            print("\n")
        raise BeancountError(posting.meta, str(e), tx_orig, named_tuple)
