from typing import List, Dict, Tuple, Set
from collections import namedtuple
import os.path
from beancount.core.data import Directive, Custom, Open
from beancount.ops import validation
from beancount import loader
from autobean.utils.error_logger import ErrorLogger
from autobean.share import utils
from autobean.share.fill_residuals import fill_residuals
from autobean.share.select_viewpoint import select_viewpoint
from autobean.share.map_residual_accounts import map_residual_accounts
from autobean.share.open_subaccounts import open_subaccounts


def plugin(entries: List[Directive], options: Dict) -> Tuple[List[Directive], List]:
    errors = validation.validate(entries, options)
    if errors:
        return entries, errors
    includes = set(options['include'])
    logger = ErrorLogger()
    entries = include(entries, includes, logger)
    entries = map_residual_accounts(entries, logger)
    entries = open_subaccounts(entries, logger)
    options['include'] = list(includes)
    return entries, logger.errors


__plugins__ = [plugin]


InvalidDirectiveError = namedtuple('InvalidDirectiveError', 'source message entry')


def include(entries: List[Directive], includes: Set[str], logger: ErrorLogger) -> List[Directive]:
    ret = []
    for entry in entries:
        if isinstance(entry, Custom) and entry.type == 'autobean.share.include':
            file_entries = process_include_directive(entry, includes, logger)
            ret.extend(file_entries)
        else:
            ret.append(entry)
    ret = deduplicate_opens(ret)
    return ret


def process_include_directive(entry: Custom, includes: Set[str], logger: ErrorLogger) -> List[Directive]:
    if len(entry.values) != 2:
        logger.log_error(InvalidDirectiveError(
            entry.meta, 'autobean.share.include expects 2 argument but {} are given'.format(len(entry.values)), entry
        ))
        return []
    if entry.values[0].dtype is not str or entry.values[1].dtype is not str:
        logger.log_error(InvalidDirectiveError(
            entry.meta, 'autobean.share.include expects a path and a viewpoint as arguments', entry
        ))
        return []
    path = entry.values[0].value
    path = os.path.join(os.path.dirname(entry.meta['filename']), path)
    entries, errors, options = loader.load_file(path)
    logger.log_loading_errors(errors, entry)
    includes.update(set(options['include']))
    viewpoint = entry.values[1].value
    entries = transform_external_ledger(entries, viewpoint, includes, logger)
    return entries


def filter_out_share_directives(entries: List[Directive]) -> List[Directive]:
    return [
        entry
        for entry in entries
        if not utils.is_autobean_share_directive(entry)
    ]


def transform_external_ledger(entries: List[Directive], viewpoint: str, includes: Set[str], logger: ErrorLogger) -> List[Directive]:
    entries = include(entries, includes, logger)
    entries = fill_residuals(entries, logger)
    entries = select_viewpoint(entries, viewpoint, logger)
    entries = filter_out_share_directives(entries)
    return entries


def deduplicate_opens(entries: List[Directive]) -> List[Directive]:
    ret = []
    open_accounts = set()
    for entry in entries:
        if not isinstance(entry, Open):
            ret.append(entry)
        elif entry.account not in open_accounts:
            open_accounts.add(entry.account)
            ret.append(entry)
    return ret
