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
        (Dialect.postgresql, "tests/testdata/models/ddl_postgres.sql"),
        (Dialect.mysql, "tests/testdata/models/ddl_mysql.sql"),
    ],
)
def test_run_models(
    dialect: Dialect,
    expected_ddl_file: str,
    capsys: CaptureFixture,
) -> None:
    with open(expected_ddl_file, "r") as f:
        expected_ddl = f.read().replace("[ABS_PATH]", str(Path.cwd()))
    metadata = run(dialect, [Path("tests/testdata/models")])
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    for m in metadata:
        m.clear()


@pytest.mark.parametrize(
    "dialect, expected_ddl_file",
    [
        (Dialect.postgresql, "tests/testdata/old_models/ddl_postgres.sql"),
        (Dialect.mysql, "tests/testdata/old_models/ddl_mysql.sql"),
    ],
)
def test_run_old_models(
    dialect: Dialect,
    expected_ddl_file: str,
    capsys: CaptureFixture,
) -> None:
    with open(expected_ddl_file, "r") as f:
        expected_ddl = f.read().replace("[ABS_PATH]", str(Path.cwd()))
    metadata = run(dialect, [Path("tests/testdata/old_models")])
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    for m in metadata:
        m.clear()


@pytest.mark.parametrize(
    "dialect, expected_ddl_file",
    [
        (Dialect.postgresql, "tests/testdata/structured_models/ddl_postgres.sql"),
        (Dialect.mysql, "tests/testdata/structured_models/ddl_mysql.sql"),
    ],
)
def test_run_structured_models(
    dialect: Dialect,
    expected_ddl_file: str,
    capsys: CaptureFixture,
) -> None:
    with open(expected_ddl_file, "r") as f:
        expected_ddl = f.read().replace("[ABS_PATH]", str(Path.cwd()))
    metadata = run(dialect, [Path("tests/testdata/structured_models/models")])
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    for m in metadata:
        m.clear()


@pytest.mark.parametrize(
    "dialect",
    [Dialect.postgresql, Dialect.mysql],
)
def test_run_multiple_paths(
    dialect: Dialect,
    capsys: CaptureFixture,
) -> None:
    with open(f"tests/testdata/multi_path/ddl_{dialect.value}.sql", "r") as f:
        expected_ddl = f.read().replace("[ABS_PATH]", str(Path.cwd()))
    metadata = run(
        dialect,
        [
            Path("tests/testdata/multi_path/models1"),
            Path("tests/testdata/multi_path/models2"),
        ],
    )
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    for m in metadata:
        m.clear()


@pytest.mark.parametrize(
    "dialect, expected_ddl_file",
    [
        (Dialect.postgresql, "tests/testdata/tables/ddl_postgres.sql"),
        (Dialect.mysql, "tests/testdata/tables/ddl_mysql.sql"),
    ],
)
def test_run_models_2(
    dialect: Dialect,
    expected_ddl_file: str,
    capsys: CaptureFixture,
) -> None:
    with open(expected_ddl_file, "r") as f:
        expected_ddl = f.read().replace("[ABS_PATH]", str(Path.cwd()))
    metadata = run(dialect, [Path("tests/testdata/tables")])
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    for m in metadata:
        m.clear()


def test_get_old_metadata() -> None:
    metadata = get_metadata(Path("tests/testdata/old_models"))
    assert isinstance(metadata, MetaData)
    metadata.clear()


@pytest.mark.skipif(
    sqlalchemy_version() < (2, 0),
    reason="requires SQLAlchemy>=2.0",
)
def test_get_metadata_explicit_path() -> None:
    metadata = get_metadata(Path("tests/testdata/models"))
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
        get_metadata(Path("tests/testdata/invalid_models"))


@pytest.mark.skipif(
    sqlalchemy_version() < (2, 0),
    reason="requires SQLAlchemy>=2.0",
)
def test_get_metadata_invalid_models_skip_errors() -> None:
    metadata = get_metadata(Path("tests/testdata/invalid_models"), skip_errors=True)
    assert isinstance(metadata, MetaData)
    metadata.clear()
