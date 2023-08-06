from collections import namedtuple
from typing import List, Optional
from beancount.core.data import Directive, Balance, Transaction
from autobean.utils.error_logger import ErrorLogger
from autobean.share import utils


InvalidDirectiveError = namedtuple('InvalidDirectiveError', 'source message entry')
DuplicatedOwnerError = namedtuple('InvalidDirectiveError', 'source message entry')


def select_viewpoint(entries: List[Directive], viewpoint: Optional[str], logger: ErrorLogger) -> List[Directive]:
    if viewpoint is None:
        return entries
    ret = []
    is_owner = viewpoint == get_owner(entries, logger)
    for entry in entries:
        if isinstance(entry, Balance):
            continue
        if isinstance(entry, Transaction):
            entry = process_transaction(entry, viewpoint, is_owner)
        ret.append(entry)
    return ret


def process_transaction(entry: Transaction, viewpoint: str, is_owner: bool) -> Transaction:
    if is_owner:
        postings = []
        for posting in entry.postings:
            is_residuals = posting.account.startswith('[Residuals]:')
            is_mine = posting.account.endswith(f':[{viewpoint}]')
            if is_residuals and not is_mine:
                posting = posting._replace(
                    account=posting.account,
                    units=-posting.units,
                )
                postings.append(posting)
            elif is_mine and not is_residuals:
                posting = posting._replace(
                    account=posting.account.rsplit(':', 1)[0],
                )
                postings.append(posting)
    else:
        postings = [
            posting._replace(
                account=posting.account.rsplit(':', 1)[0],
            )
            for posting in entry.postings
            if posting.account.endswith(f':[{viewpoint}]')
        ]
    return entry._replace(
        postings=postings,
    )


def get_owner(entries: List[Directive], logger: ErrorLogger) -> Optional[str]:
    entries = [entry for entry in entries if utils.is_owner_directive(entry)]
    if not entries:
        return None
    for entry in entries:
        if len(entry.values) != 1:
            logger.log_error(InvalidDirectiveError(
                entry.meta, 'autobean.share.owner expects 1 argument but {} are given'.format(len(entry.values)), entry
            ))
        if entry.values[0].dtype is not str:
            logger.log_error(InvalidDirectiveError(
                entry.meta, 'autobean.share.owner expects a name as argument', entry
            ))
    if len(entries) > 1:
        for entry in entries[1:]:
            logger.log_error(DuplicatedOwnerError(
                entry.meta, 'Duplicated autobean.share.owner directive', entry
            ))
    return entries[0].values[0].value
