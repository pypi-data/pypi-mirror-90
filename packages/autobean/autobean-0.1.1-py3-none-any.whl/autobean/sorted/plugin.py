from collections import defaultdict, namedtuple
from typing import List, Dict, Tuple, Set, Any
from beancount.core.data import Directive, Transaction, Custom
from autobean.narration import comments


InvalidDirectiveError = namedtuple('OutOfOrderDirectiveError', 'source message entry')
OutOfOrderDirectiveError = namedtuple('OutOfOrderDirectiveError', 'source message entry')


def plugin(entries: List[Directive], options: Dict) -> Tuple[List[Directive], List[Any]]:
    entries_by_file = defaultdict(list)
    ignored_files = set()
    errors = []
    for entry in entries:
        # Plugin-generated entries may not have associated file or line number.
        # We ignore entries in either case.
        if (hasattr(entry, 'date') and
                hasattr(entry, 'meta') and
                entry.meta.get('filename', None) and
                entry.meta.get('lineno', None)):
            should_append = True
            if is_enabling_directive(entry):
                if len(entry.values) != 1 or entry.values[0].dtype != bool:
                    errors.append(InvalidDirectiveError(
                        entry.meta,
                        'autobean.sorted.enabled directive accepts a single '
                        'boolean argument',
                        entry))
                    should_append = False
            if should_append:
                entries_by_file[entry.meta['filename']].append(entry)

    # ignores entries with no filename or no line number
    entries_by_file.pop(None, None)
    for filename, file_entries in entries_by_file.items():
        if filename not in ignored_files:
            errors.extend(check_file_entries(file_entries))
    return entries, errors
    

def is_enabling_directive(entry: Directive) -> bool:
    return isinstance(entry, Custom) and entry.type == 'autobean.sorted.enabled'


def check_file_entries(entries: List[Directive]) -> List[Any]:
    """Checks entries are in order and finds out-of-order entries.

    We find a longest non-descending subsequence and assumes all other
    entries are out-of-order.

    When finding the longest non-descending subsequence, we prefer the one
    whose maximum date is minimal. For example, in time sequence 1 2 100 3
    it's more likely that 1 2 3 is correct and 100 is a mistake (compared to
    1 2 100 as correct and 3 as mistake).
    """

    prevs = []
    # [(length, -maxdate)]
    scores = []

    sorted_entries = []
    enabled = True
    for entry in sorted(entries, key=lambda e: e.meta['lineno']):
        if is_enabling_directive(entry):
            enabled = entry.values[0].value
            continue
        if enabled:
            sorted_entries.append(entry)

    global_best_i = None

    for entry in sorted_entries:
        best = (1, -entry.date.toordinal())
        prev = None
        for i, score in enumerate(scores):
            if sorted_entries[i].date <= entry.date:
                current = (
                    score[0] + 1,
                    max(score[1], -sorted_entries[i].date.toordinal()))
                if current > best:
                    best = current
                    prev = i
        scores.append(best)
        prevs.append(prev)
        if global_best_i is None or best > scores[global_best_i]:
            global_best_i = len(scores) - 1
    prevs.append(global_best_i)

    misplaced_entries = []
    i = len(prevs) - 1
    while prevs[i] is not None:
        j = prevs[i]
        for k in range(i - 1, j, -1):
            misplaced_entries.append(sorted_entries[k])
        i = j

    errors = []
    for misplaced_entry in misplaced_entries[::-1]:
        errors.append(OutOfOrderDirectiveError(
            misplaced_entry.meta,
            'Directive date does not follow non-descending order within the '
            'file',
            misplaced_entry))
    
    return errors
