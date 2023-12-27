from cli.main import run, get_declarative_base, ModelsNotFoundError
from pathlib import Path
from sqlalchemy.orm import DeclarativeBase
import pytest

POSTGRES_DIALECT = 'postgresql+psycopg2'
MYSQL_DIALECT = 'mysql+pymysql'


def test_run_postgres(capsys):
    with open('tests/ddl_postgres.sql', 'r') as f:
        expected_ddl = f.read()
    base = run(POSTGRES_DIALECT, "tests/models")
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    base.metadata.clear()


def test_run_mysql(capsys):
    with open('tests/ddl_mysql.sql', 'r') as f:
        expected_ddl = f.read()
    base = run(MYSQL_DIALECT, "tests/models")
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    base.metadata.clear()


def test_get_declarative_base():
    base = get_declarative_base(Path("tests"))
    assert issubclass(base, DeclarativeBase)
    base.metadata.clear()


def test_get_declarative_base_explicit_path():
    base = get_declarative_base(Path("tests/models"))
    assert issubclass(base, DeclarativeBase)
    base.metadata.clear()


def test_get_declarative_base_explicit_path_fail():
    with pytest.raises(ModelsNotFoundError, match='Found no sqlalchemy models in the directory tree.'):
        base = get_declarative_base(Path("nothing/here"))
        base.metadata.clear()
