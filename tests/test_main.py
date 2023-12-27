from cli.main import run, get_declarative_base, ModelsNotFoundError
from sqlalchemy.orm import DeclarativeBase
import os
import pytest

POSTGRES_DIALECT = 'postgresql+psycopg2'
MYSQL_DIALECT = 'mysql+pymysql'


def test_run_postgres(capsys):
    capsys.readouterr()
    with open('tests/ddl_postgres.sql', 'r') as f:
        expected_ddl = f.read()
    base = run(POSTGRES_DIALECT)
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    capsys.close()
    base.metadata.clear()


def test_run_mysql(capsys):
    capsys.readouterr()
    with open('tests/ddl_mysql.sql', 'r') as f:
        expected_ddl = f.read()
    base = run(MYSQL_DIALECT)
    captured = capsys.readouterr()
    assert captured.out == expected_ddl
    capsys.close()
    base.metadata.clear()


def test_get_declarative_base():
    models_dir = os.getcwd()
    base = get_declarative_base(models_dir)
    assert issubclass(base, DeclarativeBase)
    base.metadata.clear()


def test_get_declarative_base_explicit_path():
    models_dir = os.getcwd() + '/tests/models'
    base = get_declarative_base(models_dir)
    assert issubclass(base, DeclarativeBase)
    base.metadata.clear()


def test_get_declarative_base_explicit_path_fail():
    models_dir = os.getcwd() + '/nothing/here'
    with pytest.raises(ModelsNotFoundError, match='Found no sqlalchemy models in the directory tree.'):
        base = get_declarative_base(models_dir)
        base.metadata.clear()


def test_get_declarative_base_debug_empty(capsys):
    capsys.readouterr()
    models_dir = os.getcwd()
    base = get_declarative_base(models_dir, debug=True)
    captured = capsys.readouterr()
    assert captured.out == ''
    capsys.close()
    base.metadata.clear()
