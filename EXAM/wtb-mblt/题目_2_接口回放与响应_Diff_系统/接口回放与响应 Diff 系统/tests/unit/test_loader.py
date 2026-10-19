from copy import deepcopy
from decimal import Decimal

import pytest
import simplejson

from response_diff.config import Limits
from response_diff.errors import InputValidationError, LimitExceededError
from response_diff.jsonio import read_json
from response_diff.loader import load_snapshot, validate_records, validate_tree
from tests.support import record, write_json


@pytest.mark.parametrize("data", [None, {}, [1], [{}], [record({}, record_id="")], [record({}, record_id=1)], [record({}, description=None)], [record({}, method="get")], [record({}, method=1)], [record({}, path="relative")], [record({}, path=None)], [record({}, status=True)], [record({}, status=Decimal("200.0"))], [record({}, status=99)], [record({}, status=600)]])
def test_invalid_records(data):
    with pytest.raises(InputValidationError):
        validate_records(data, Limits(), "测试输入")


@pytest.mark.parametrize("field", ["request", "response"])
def test_wrong_nested_record(field):
    data = record({})
    data[field] = []
    with pytest.raises(InputValidationError):
        validate_records([data], Limits(), "测试输入")


def test_missing_body_and_duplicate_id():
    data = record({})
    del data["response"]["body"]
    with pytest.raises(InputValidationError, match="body"):
        validate_records([data], Limits(), "测试输入")
    with pytest.raises(InputValidationError, match="重复"):
        validate_records([record({}), record({})], Limits(), "测试输入")


@pytest.mark.parametrize("content", [b'{"x":1,"x":2}', b'NaN', b'Infinity', b'-Infinity', b'{', b'[] trailing', b'\xff'])
def test_invalid_json_files(tmp_path, content):
    path = tmp_path / "input.json"
    path.write_bytes(content)
    with pytest.raises((InputValidationError, simplejson.JSONDecodeError, UnicodeDecodeError)):
        read_json(path, 10000)


def test_utf8_bom_and_precision(tmp_path):
    path = write_json(tmp_path / "中文 input.json", [record({"文字": "中文\n内容", "number": Decimal("0.123456789012345678901234567890")})])
    path.write_bytes(b'\xef\xbb\xbf' + path.read_bytes())
    snapshot = load_snapshot(path, Limits())
    assert snapshot.records["r"].body["number"] == Decimal("0.123456789012345678901234567890")
    assert snapshot.records["r"].body["文字"] == "中文\n内容"


def test_invalid_unicode_and_runtime_values(tmp_path):
    path = tmp_path / "surrogate.json"
    path.write_bytes(br'[{"id":"r","description":"test","request":{"method":"GET","path":"/"},"response":{"status":200,"body":"\uD800"}}]')
    with pytest.raises(UnicodeEncodeError):
        load_snapshot(path, Limits())
    with pytest.raises(InputValidationError, match="有限"):
        validate_tree(Decimal("NaN"), Limits(), "测试输入")
    with pytest.raises(InputValidationError, match="字段名称"):
        validate_tree({1: "x"}, Limits(), "测试输入")


def test_limits_boundaries(tmp_path):
    path = tmp_path / "input.json"
    path.write_bytes(b'[]')
    assert read_json(path, 2)[0] == []
    with pytest.raises(LimitExceededError, match="max_file_bytes"):
        read_json(path, 1)
    validate_records([record({})], Limits(max_records=1), "测试输入")
    with pytest.raises(LimitExceededError, match="max_records"):
        validate_records([record({}, "a"), record({}, "b")], Limits(max_records=1), "测试输入")
    validate_tree({"x": 1}, Limits(max_nodes=2), "测试输入")
    with pytest.raises(LimitExceededError, match="max_nodes"):
        validate_tree({"x": 1}, Limits(max_nodes=1), "测试输入")
    validate_tree({"x": {"y": 1}}, Limits(max_depth=2), "测试输入", True)
    with pytest.raises(LimitExceededError, match="max_depth"):
        validate_tree({"x": {"y": 1}}, Limits(max_depth=1), "测试输入", True)
    validate_tree([1], Limits(max_array_items=1), "测试输入", True)
    with pytest.raises(LimitExceededError, match="max_array_items"):
        validate_tree([1, 2], Limits(max_array_items=1), "测试输入", True)


def test_file_errors_and_parser_depth(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_snapshot(tmp_path / "missing.json", Limits())
    with pytest.raises(OSError):
        load_snapshot(tmp_path, Limits())
    path = tmp_path / "deep.json"
    nested = 0
    for _ in range(150):
        nested = [nested]
    write_json(path, [record(nested)])
    with pytest.raises(LimitExceededError, match="max_depth"):
        load_snapshot(path, Limits())


def test_metadata_and_input_protection():
    rows = [record({}, description="")]
    rows[0]["extra"] = {"unicode": "中文"}
    saved = deepcopy(rows)
    assert validate_records(rows, Limits(), "测试输入")["r"].description == ""
    assert rows == saved
