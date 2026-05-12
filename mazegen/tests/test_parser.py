from ..config.parser import parse_config, parse_coordinate
import pytest


def test_parse_config_valid_input() -> None:
    content = [
        "WIDTH=10",
        "HEIGHT=20",
    ]

    config, errors = parse_config(content)

    assert config == {"WIDTH": "10", "HEIGHT": "20"}
    assert errors == []


def test_parse_config_ignores_comments_and_empty() -> None:
    content = [
        "# comment",
        "",
        "KEY=VALUE",
    ]

    config, errors = parse_config(content)

    assert config == {"KEY": "VALUE"}
    assert errors == []


def test_parse_config_missing_equal() -> None:
    content = ["INVALID_LINE"]

    config, errors = parse_config(content)

    assert config == {}
    assert len(errors) == 1
    assert "SYNTAX ERROR" in errors[0]


def test_parse_config_missing_key() -> None:
    content = ["=10"]

    config, errors = parse_config(content)

    assert config == {}
    assert any("Missing key" in e for e in errors)


def test_parse_config_missing_value() -> None:
    content = ["KEY="]

    config, errors = parse_config(content)

    assert config == {}
    assert any("Missing value" in e for e in errors)


def test_parse_config_duplicate_keys() -> None:
    content = [
        "KEY=1",
        "KEY=2",
    ]

    config, errors = parse_config(content)

    assert config == {"KEY": "1"}
    assert any("Duplicate key" in e for e in errors)


def test_parse_coordinate_valid() -> None:
    assert parse_coordinate("1,2") == (2, 1)


def test_parse_coordinate_invalid_format() -> None:
    with pytest.raises(ValueError):
        parse_coordinate("invalid")


def test_parse_coordinate_non_numeric() -> None:
    with pytest.raises(ValueError):
        parse_coordinate("a,b")
