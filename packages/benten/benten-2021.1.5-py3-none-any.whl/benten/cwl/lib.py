#  Copyright (c) 2019 Seven Bridges. See LICENSE

import pathlib
import urllib.parse
import urllib.request
import urllib.error

from ..langserver.lspobjects import Diagnostic, DiagnosticSeverity, Range, Position
from ..code.yaml import fast_yaml_load


def get_range_for_key(parent, key):
    start = parent.lc.key(key)
    end = (start[0], start[1] + len(key))
    return Range(Position(*start), Position(*end))


# TODO: refactor this for redundancy
def get_range_for_value(node, key):
    if isinstance(node, dict):
        start = node.lc.value(key)
    else:
        start = node.lc.item(key)

    v = node[key]
    if v is None:
        end = (start[0], start[1])
    else:
        v = str(v)
        _lines = v.splitlines() or [""]
        ln_cnt = len(_lines)
        if ln_cnt == 1:
            ln_cnt -= 1
        # Multi-line strings begin from the next line as opposed to single line strings

        # Ideally we'd be carrying around the raw lines to compute the end of the last line
        # but this is good enough and less cumbersome
        end = (start[0] + ln_cnt, (len(_lines[-1]) + start[1]) if ln_cnt == 0 else 1000)

    return Range(Position(*start), Position(*end))


class ListOrMap:

    def __init__(self, node, key_field, problems):
        self.was_dict = None
        self.as_dict = {}
        self.original_obj = node
        self.key_ids = {}
        self.map_key_to_idx = {}
        if isinstance(node, dict):
            self.as_dict = node
            self.was_dict = True
        elif isinstance(node, list):
            self.was_dict = False
            for n, _item in enumerate(node):
                if isinstance(_item, dict):
                    key = _item.get(key_field)
                    if key is not None:
                        self.as_dict[key] = _item
                        self.key_ids[key] = get_range_for_value(_item, key_field)
                        self.map_key_to_idx[key] = n
                        continue

                    # Exception to handle $import
                    # see https://github.com/common-workflow-language/common-workflow-language/issues/896
                    if "$import" in _item:
                        key = "class"
                        self.as_dict[key] = _item
                        self.key_ids[key] = get_range_for_value(_item, "$import")
                        self.map_key_to_idx[key] = n
                        continue

                    problems += [
                        Diagnostic(
                            _range=get_range_for_value(node, n),
                            message=f"Missing key field {key_field}",
                            severity=DiagnosticSeverity.Error)
                    ]

    def get_range_for_id(self, key):
        if self.was_dict:
            return get_range_for_key(self.as_dict, key)
        else:
            return self.key_ids[key]

    def get_range_for_value(self, key):
        if self.was_dict:
            return get_range_for_value(self.as_dict, key)
        else:
            return get_range_for_value(self.original_obj, self.map_key_to_idx[key])


# TODO: Deprecate this function
def list_as_map(node, key_field, problems):
    if isinstance(node, dict):
        return node

    new_node = {}

    if isinstance(node, list):
        for n, _item in enumerate(node):
            if isinstance(_item, dict):
                key = _item.get(key_field)
                if key is not None:
                    new_node[key] = _item
                else:
                    problems += [
                        Diagnostic(
                            _range=get_range_for_value(node, n),
                            message=f"Missing key field {key_field}",
                            severity=DiagnosticSeverity.Error)
                    ]

    return new_node


def validate_and_load_linked_file(doc_uri: str, path: str, loc: Range, problems: list) -> (str, str, dict):

    link_url = urllib.parse.urlparse(path)
    full_path, contents, node_dict = link_url.path, "", {}

    if link_url.scheme not in ["file://", ""]:
        try:
            contents = urllib.request.urlopen(path).read().decode('utf-8')
            node_dict = fast_yaml_load(contents)
        except urllib.error.HTTPError:
            problems += [
                Diagnostic(
                    _range=loc,
                    message=f"Missing URL: {path}",
                    severity=DiagnosticSeverity.Error)
            ]

        return path, contents, node_dict

    linked_file = resolve_file_path(doc_uri, path)
    if not linked_file.exists():
        problems += [
            Diagnostic(
                _range=loc,
                message=f"Missing document: {path}",
                severity=DiagnosticSeverity.Error)
        ]
    elif not linked_file.is_file():
        problems += [
            Diagnostic(
                _range=loc,
                message=f"Linked document must be file: {path}",
                severity=DiagnosticSeverity.Error)
        ]
    else:
        contents = linked_file.open("r").read()
        node_dict = fast_yaml_load(contents)

    return linked_file, contents, node_dict


def normalized_path(doc_uri: str, path: str):
    link_url = urllib.parse.urlparse(path)
    if link_url.scheme not in ["file://", ""]:
        return path
    else:
        return str(resolve_file_path(doc_uri, path))


# doc_uri on windows takes the form "file:///c%3A/Users/me/a.cwl"
# parsing the uri into components results in path being "/c%3A/Users/me/a.cwl"
# This needs to be
# a) decoded (so that c%3A -> c:)
# b) The leading "/" needs to be chomped.
# Step a) is redundant on *nix and b) should not be done
def un_mangle_uri(doc_uri):
    _my_path = pathlib.Path(urllib.parse.unquote(urllib.parse.urlparse(doc_uri).path))
    if isinstance(_my_path, pathlib.WindowsPath):
        _my_path = pathlib.Path(str(_my_path)[1:])
    return _my_path


def resolve_file_path(doc_uri, target_path):
    _path = pathlib.PurePosixPath(target_path)
    if not _path.is_absolute():
        base_path = un_mangle_uri(doc_uri).parent
    else:
        base_path = "."
    _path = pathlib.Path(base_path / _path).resolve().absolute()
    return _path


def normalize_source(src):
    if isinstance(src, str) and src.startswith("#"):
        return src[1:]
    else:
        return src
