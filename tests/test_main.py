from pathlib import Path

import pytest
from pytest import CaptureFixture
from sqlalchemy import MetaData

from atlas_provider_sqlalchemy.ddl import sqlalchemy_version
from atlas_provider_sqlalchemy.main import (
    Dialect,
    ModuleImportError,
    ModelsNotFoundError,
    get_metadata,
    run,
)

@pytest.mark.skipif(
    sqlalchemy_version() < (2, 0),
    reason="requires SQLAlchemy>=2.0",
)
@pytest.mark.parametrize(
    "dialect, expected_ddl_file",
    [
        (Dialect.postgresql, "tests/models/ddl_postgres.sql"),
        (Dialect.mysql, "tests/models/ddl_mysql.sql"),
    ],
)
def test_run_models(
    dialect: Dialect,
    expected_ddl_file: str,
    capsys: CaptureFixture,
) -> None:
    with open(expected_ddl_file, "r") as f:
        expected_ddl = f.read().replace("[ABS_PATH]",str(Path.cwd()))
    metadata = run(dialect, Path("tests/models"))
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    metadata.clear()


@pytest.mark.parametrize(
    "dialect, expected_ddl_file",
    [
        (Dialect.postgresql, "tests/old_models/ddl_postgres.sql"),
        (Dialect.mysql, "tests/old_models/ddl_mysql.sql"),
    ],
)
def test_run_old_models(
    dialect: Dialect,
    expected_ddl_file: str,
    capsys: CaptureFixture,
) -> None:
    with open(expected_ddl_file, "r") as f:
        expected_ddl = f.read().replace("[ABS_PATH]",str(Path.cwd()))
    metadata = run(dialect, Path("tests/old_models"))
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    metadata.clear()

@pytest.mark.parametrize(
    "dialect, expected_ddl_file",
    [
        (Dialect.postgresql, "tests/structured_models/ddl_postgres.sql"),
        (Dialect.mysql, "tests/structured_models/ddl_mysql.sql"),
    ],
)
def test_run_structured_models(
    dialect: Dialect,
    expected_ddl_file: str,
    capsys: CaptureFixture,
) -> None:
    with open(expected_ddl_file, "r") as f:
        expected_ddl = f.read().replace("[ABS_PATH]",str(Path.cwd()))
    metadata = run(dialect, Path("tests/structured_models/models"))
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    metadata.clear()


@pytest.mark.parametrize(
    "dialect, expected_ddl_file",
    [
        (Dialect.postgresql, "tests/tables/ddl_postgres.sql"),
        (Dialect.mysql, "tests/tables/ddl_mysql.sql"),
    ],
)
def test_run_models_2(
    dialect: Dialect,
    expected_ddl_file: str,
    capsys: CaptureFixture,
) -> None:
    with open(expected_ddl_file, "r") as f:
        expected_ddl = f.read().replace("[ABS_PATH]",str(Path.cwd()))
    metadata = run(dialect, Path("tests/tables"))
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    metadata.clear()


def test_get_old_metadata() -> None:
    metadata = get_metadata(Path("tests/old_models"))
    assert isinstance(metadata, MetaData)
    metadata.clear()


@pytest.mark.skipif(
    sqlalchemy_version() < (2, 0),
    reason="requires SQLAlchemy>=2.0",
)
def test_get_metadata_explicit_path() -> None:
    metadata = get_metadata(Path("tests/models"))
    assert isinstance(metadata, MetaData)
    metadata.clear()


def test_get_metadata_explicit_path_fail() -> None:
    with pytest.raises(ModelsNotFoundError):
        get_metadata(Path("nothing/here"))


@pytest.mark.skipif(
    sqlalchemy_version() < (2, 0),
    reason="requires SQLAlchemy>=2.0",
)
def test_get_metadata_invalid_models() -> None:
    with pytest.raises(ModuleImportError):
        get_metadata(Path("tests/invalid_models"))


@pytest.mark.skipif(
    sqlalchemy_version() < (2, 0),
    reason="requires SQLAlchemy>=2.0",
)
def test_get_metadata_invalid_models_skip_errors() -> None:
    metadata = get_metadata(Path("tests/invalid_models"), skip_errors=True)
    assert isinstance(metadata, MetaData)
    metadata.clear()
