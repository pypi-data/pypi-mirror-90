''' Helper functions that don't quite fit elsewhere '''
import re
from typing import Tuple
from urllib.parse import quote, unquote, urlsplit
from urllib.request import url2pathname

from yarals.base import protocol as lsp


def create_file_uri(path: str):
    '''Create a URI given a file path

    :path: Filepath to create a URI from
    '''
    # if this is a windows path, the slashes need to be reversed
    return "file://{}".format(quote(str(path).replace("\\", "/"), safe="/\\"))

def get_first_non_whitespace_index(line: str) -> int:
    '''Get the first non-whitespace character index in a given line

    :line: Text line to parse
    '''
    for index, char in enumerate(line):
        if char.strip():
            # self._logger.debug("first char is {} at position {:d}".format(char, index))
            return index

def get_rule_range(document: str, pos: lsp.Position) -> lsp.Range:
    '''Get the range of the YARA rule that a given symbol is in

    :document: Text to search in
               To determine line numbers, text is split at newlines, and carriage returns are ignored
    :pos: Symbol position to base range off of
    '''
    start_pattern = re.compile(r"^((private|global) )?rule\b")
    end_pattern = re.compile("^}$")
    lines = document.replace("\r", "").split("\n")
    # default to assuming the entire document is within range
    start_pos = lsp.Position(line=0, char=0)
    end_pos = lsp.Position(line=len(lines), char=0)
    # work backwards from the given position and find the start of rule
    for index in range(pos.line, 0, -1):
        line = lines[index]
        match = start_pattern.match(line)
        if match:
            start_pos = lsp.Position(line=index, char=0)
            break
    # start from the given position and find the first end of rule
    for index in range(pos.line, len(lines)):
        line = lines[index]
        match = end_pattern.match(line)
        if match:
            end_pos = lsp.Position(line=index, char=0)
            break
    return lsp.Range(start=start_pos, end=end_pos)

def parse_result(result: str) -> Tuple[int,str]:
    '''Parse the results from a YARA compilation attempt

    :result: Text to parse - takes the form:
            "line {number}: {message}"
    '''
    meta, message = tuple(result.split(":", maxsplit=1))
    _, line_no = tuple(meta.split(" "))
    return int(line_no), message.strip()

def parse_uri(uri: str, encoding="utf-8"):
    '''Parse a path out of a given uri

    :uri: URI string to be parsed
    :encoding: (Optional) string encoding to parse with
    '''
    if uri:
        url = urlsplit(unquote(uri, encoding=encoding))
        return url2pathname(url.path)

def resolve_symbol(document: str, pos: lsp.Position) -> str:
    '''Resolve a symbol located at the given position

    :document: Text to search in
               To determine line numbers, text is split at newlines, and carriage returns are ignored
    :pos: Symbol position to base range off of
    '''
    try:
        symbol_line = document.split("\n")[pos.line]
        line_end = len(symbol_line)
        # find the left-bound of the symbol by looking backwards until a whitespace
        index = pos.char - 1
        while True:
            if index == 0 \
            or not symbol_line[index].strip():
                # whitespace found - left-bound, is one char to the right
                left_bound = index + 1
                break
            index -= 1
        # find the right-bound of the symbol by looking forwards until a whitespace or a non-alphanum/special char
        index = pos.char
        while True:
            if index == line_end \
            or not symbol_line[index].strip() \
            or not (symbol_line[index].isalnum() or symbol_line[index] in "_*"):
                right_bound = index
                break
            index += 1
        return symbol_line[left_bound:right_bound]
    except IndexError:
        return ""
