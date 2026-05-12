from ..config.caster import cast_config
from ..config import get_config, ConfigError
import pytest


def test_cast_config_valid() -> None:
    raw = {
        "WIDTH": "10",
        "HEIGHT": "20",
        "ENTRY": "1,2",
        "EXIT": "3,4",
        "OUTPUT_FILE": "out.txt",
        "PERFECT": "true",
    }

    config = cast_config(raw)

    assert config["WIDTH"] == 10
    assert config["HEIGHT"] == 20
    assert config["ENTRY"] == (2, 1)
    assert config["EXIT"] == (4, 3)
    assert config["OUTPUT_FILE"] == "out.txt"
    assert config["PERFECT"] is True


def test_cast_config_false_boolean() -> None:
    raw = {
        "WIDTH": "1",
        "HEIGHT": "1",
        "ENTRY": "0,0",
        "EXIT": "0,0",
        "OUTPUT_FILE": "x",
        "PERFECT": "false",
    }

    config = cast_config(raw)

    assert config["PERFECT"] is False


def test_get_config_valid_flow() -> None:
    content = [
        "WIDTH=10",
        "HEIGHT=10",
        "ENTRY=0,0",
        "EXIT=9,9",
        "OUTPUT_FILE=out.txt",
        "PERFECT=true",
    ]

    config = get_config(content)

    assert config["WIDTH"] == 10
    assert config["HEIGHT"] == 10
    assert config["ENTRY"] == (0, 0)
    assert config["EXIT"] == (9, 9)
    assert config["PERFECT"] is True


def test_get_config_invalid_parsing() -> None:
    content = [
        "WIDTH=10",
        "INVALID_LINE",
    ]

    with pytest.raises(ConfigError):
        get_config(content)


def test_get_config_validation_error(monkeypatch: pytest.MonkeyPatch) -> None:
    from ..config import get_config

    def fake_validation() -> list[str]:
        return ["fake error"]

    monkeypatch.setattr(
        "mazegen.config.validator.get_validation_errors",
        fake_validation
    )

    content = [
        "WIDTH=10",
        "HEIGHT=10",
        "ENTRY=0,0",
        "EXIT=1,1",
        "OUTPUT_FILE=x",
        "PERFECT=true",
    ]

    try:
        get_config(content)
        assert False, "Should raise ConfigError"
    except Exception as e:
        assert "fake error" in str(e)


def test_config_error_contains_all_messages() -> None:
    try:
        raise ConfigError("error1\n- error2")
    except ConfigError as e:
        assert "error1" in str(e)
        assert "error2" in str(e)
