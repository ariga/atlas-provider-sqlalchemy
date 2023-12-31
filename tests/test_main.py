from atlas_provider_sqlalchemy.main import run, get_declarative_base, Dialect
from pathlib import Path
from sqlalchemy.orm import DeclarativeBase
import pytest


def test_run_postgres(capsys):
    with open('tests/ddl_postgres.sql', 'r') as f:
        expected_ddl = f.read()
    base = run(Dialect.postgresql, Path("tests/models"))
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    base.metadata.clear()


def test_run_mysql(capsys):
    with open('tests/ddl_mysql.sql', 'r') as f:
        expected_ddl = f.read()
    base = run(Dialect.mysql, Path("tests/models"))
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    base.metadata.clear()


def test_run_old_declarative_base(capsys):
    with open('tests/ddl_mysql.sql', 'r') as f:
        expected_ddl = f.read()
    base = run(Dialect.mysql, Path("tests/old_models"))
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    base.metadata.clear()


def test_get_old_declarative_base():
    base = get_declarative_base(Path("tests/old_models"))
    assert not issubclass(base, DeclarativeBase)
    base.metadata.clear()


def test_get_declarative_base_explicit_path():
    base = get_declarative_base(Path("tests/models"))
    assert issubclass(base, DeclarativeBase)
    base.metadata.clear()


def test_get_declarative_base_explicit_path_fail(capsys):
    with pytest.raises(SystemExit):
        base = get_declarative_base(Path("nothing/here"))
        base.metadata.clear()
    captured = capsys.readouterr()
    assert captured.out == 'Found no sqlalchemy models in the directory tree.\n'
