"""
spotilyzer requests CSV
"""

# system imports
import csv

# project imports
from ..json.requests import REQUESTS_KEY, POD_NAME_KEY, REPLICAS_KEY, \
    CORE_LIMIT_KEY, MEM_LIMIT_KEY

# constants
_types = (str, int, float, float)


def load_requests(frequests):
    request_list = []
    with open(frequests) as f:
        reader = csv.reader(f)
        header = reader.__next__()
        _validate_header(header, frequests)
        n = len(header)
        line = 2
        for row in reader:
            _validate_row(n, row, frequests, line)
            request = _get_request(n, header, row, frequests, line)
            request_list.append(request)
            line += 1
    _validate_pod_names(request_list, frequests)
    return {REQUESTS_KEY: request_list}


def _validate_header(header, frequests):
    if header != [POD_NAME_KEY, REPLICAS_KEY, CORE_LIMIT_KEY, MEM_LIMIT_KEY]:
        raise SyntaxError(f"invalid header in {frequests}")


def _validate_row(n, row, frequests, line):
    if len(row) != n:
        raise SyntaxError("incorrect number of entries in "
                          f"{frequests}, line {line}")


def _get_request(n, header, row, frequests, line):
    try:
        return {header[i]: _types[i](row[i]) for i in range(n)}
    except ValueError as e:
        raise SyntaxError(f"invalid type in {frequests}, line {line}: {e}")


def _validate_pod_names(request_list, frequests):
    if len(request_list) != len(set(r[POD_NAME_KEY] for r in request_list)):
        raise SyntaxError(f"pod names in {frequests} are not unique")
