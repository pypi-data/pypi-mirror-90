from typing import List, Dict, Tuple, Set
from beancount.core.data import Directive, Transaction
from autobean.narration import comments


def plugin(entries: List[Directive], options: Dict) -> Tuple[List[Directive], List]:
    filenames = collect_transaction_filenames(entries)
    comment_narrations = {
        filename: comments.extract_from_file(filename)
        for filename in filenames
    }
    return [merge_narration(entry, comment_narrations) for entry in entries], []


def collect_transaction_filenames(entries: List[Directive]) -> Set[str]:
    return set(
        entry.meta['filename']
        for entry in entries
        if isinstance(entry, Transaction) and 'filename' in entry.meta)


def merge_narration(entry: Directive, comment_narrations: Dict[str, Dict[int, str]]) -> Directive:
    if not isinstance(entry, Transaction):
        return entry
    narrations = []
    if entry.narration:
        narrations.append(entry.narration)
    for posting in entry.postings:
        if posting.meta:
            narration = posting.meta.get('narration')
            comment_narration = comment_narrations.get(posting.meta.get('filename')).get(posting.meta.get('lineno'))
            if narration is None and comment_narration:
                posting.meta['narration'] = comment_narration
                narration = comment_narration
            if narration:
                narrations.append(narration.strip())
    return entry._replace(narration=' | '.join(narrations))
