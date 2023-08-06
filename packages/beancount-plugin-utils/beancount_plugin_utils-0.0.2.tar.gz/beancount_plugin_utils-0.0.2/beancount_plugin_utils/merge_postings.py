from typing import List, Union

from beancount.core.inventory import Inventory
from beancount.core.data import (
    Account,
    Posting,
)

import beancount_plugin_utils.metaset as metaset


def merge_postings(account: Account, postings: List[Posting], meta_name: Union[str, None]) -> List[Posting]:
    """
    Merges postings with an equal account name and takes meta of the first one.
    If `meta_name` is provided, then in a way of metaset combine meta values whose keys equal to `meta_name`.

    Args:
      postings: a list of postings.
      account: an account name whose postings should be merged.
      meta_name: a key for meta values that should be combined in a way of metaset.

    Example:

    Returns:
      A list of postings.
    """
    grouped_postings = []
    share_postings = []
    share_balance = Inventory()
    meta = dict()
    for posting in postings:
        if posting.account == account:
            share_postings.append(posting)
            share_balance.add_position(posting)
            if len(meta) == 0:
                meta = posting.meta
            elif meta_name is not None:
                for mark in metaset.get(posting.meta, meta_name):
                    share_postings[0] = share_postings[0]._replace(
                        meta=metaset.add(share_postings[0].meta, meta_name, mark)
                    )
        else:
            grouped_postings.append(posting)

    if share_postings:
        for pos in share_balance:
            grouped_postings.append(Posting(account, pos.units, pos.cost, None, None, share_postings[0].meta))

    return grouped_postings
