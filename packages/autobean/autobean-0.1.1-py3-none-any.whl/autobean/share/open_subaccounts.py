from typing import List, Set, DefaultDict
from collections import defaultdict
from beancount.core.data import Directive, Transaction, Open
from autobean.utils.error_logger import ErrorLogger
from autobean.share import utils


def open_subaccounts(entries: List[Directive], logger: ErrorLogger) -> List[Directive]:
    subaccounts: DefaultDict[str, Set[str]] = defaultdict(set)
    for entry in entries:
        if not isinstance(entry, Transaction):
            continue
        for posting in entry.postings:
            if utils.is_subaccount(posting.account):
                subaccount = posting.account
                account = subaccount.rsplit(':', 1)[0]
                subaccounts[account].add(posting.account)
    ret = []
    for entry in entries:
        ret.append(entry)
        if not isinstance(entry, Open):
            continue
        for subaccount in subaccounts[entry.account]:
            ret.append(entry._replace(account=subaccount))
    return ret
