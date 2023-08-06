from beancount.core.data import Transaction
from beancount_plugin_utils import metaset
from copy import deepcopy


def strip_flaky_meta(transaction: Transaction):
    """
    From transaction and it's postings remove meta keys for 'filename', 'lineno' and '__automatic__'.
    Useful in a testsuite to compare transactions with their custom meta.

    Note: `hash_entry` from `beancount.core.compare` either takes meta into account, or not.

    Args:
        transaction [Transaction]: beancount transaction

    Returns:
        a new instance of Transaction
    """
    copy = deepcopy(transaction)

    copy = copy._replace(meta=metaset.discard(copy.meta, "filename"))
    copy = copy._replace(meta=metaset.discard(copy.meta, "lineno"))
    for j, _ in enumerate(copy.postings):
        copy.postings[j] = copy.postings[j]._replace(meta=metaset.discard(copy.postings[j].meta, "filename"))
        copy.postings[j] = copy.postings[j]._replace(meta=metaset.discard(copy.postings[j].meta, "lineno"))
        copy.postings[j] = copy.postings[j]._replace(meta=metaset.discard(copy.postings[j].meta, "__automatic__"))

    return copy
