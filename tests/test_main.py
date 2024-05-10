from pathlib import Path

import pytest
from pytest import CaptureFixture
from sqlalchemy import MetaData

from atlas_provider_sqlalchemy.main import (
    Dialect,
    ModuleImportError,
    ModelsNotFoundError,
    get_metadata,
    run,
)


@pytest.mark.parametrize(
    "dialect, expected_ddl_file",
    [
        (Dialect.postgresql, "tests/ddl_postgres.sql"),
        (Dialect.mysql, "tests/ddl_mysql.sql"),
    ],
)
@pytest.mark.parametrize(
    "db_dir",
    ["tests/models", "tests/old_models", "tests/tables"],
)
def test_run_models(
    dialect: Dialect,
    expected_ddl_file: str,
    db_dir: str,
    capsys: CaptureFixture,
) -> None:
    with open(expected_ddl_file, "r") as f:
        expected_ddl = f.read()
    metadata = run(dialect, Path(db_dir))
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    metadata.clear()


def test_get_old_metadata() -> None:
    metadata = get_metadata(Path("tests/old_models"))
    assert isinstance(metadata, MetaData)
    metadata.clear()


def test_get_metadata_explicit_path() -> None:
    metadata = get_metadata(Path("tests/models"))
    assert isinstance(metadata, MetaData)
    metadata.clear()


def test_get_metadata_explicit_path_fail() -> None:
    with pytest.raises(ModelsNotFoundError):
        get_metadata(Path("nothing/here"))


def test_get_metadata_invalid_models() -> None:
    with pytest.raises(ModuleImportError):
        get_metadata(Path("tests/invalid_models"))


def test_get_metadata_invalid_models_skip_errors() -> None:
    metadata = get_metadata(Path("tests/invalid_models"), skip_errors=True)
    assert isinstance(metadata, MetaData)
    metadata.clear()
