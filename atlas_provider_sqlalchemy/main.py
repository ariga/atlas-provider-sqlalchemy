import os
from pathlib import Path
from enum import Enum
import typer
from sqlalchemy.orm import DeclarativeBase
from typing import Type
from atlas_provider_sqlalchemy.ddl import get_declarative_base, dump_ddl

app = typer.Typer(no_args_is_help=True)


class Dialect(str, Enum):
    mysql = "mysql"
    mariadb = "mariadb"
    postgresql = "postgresql"
    sqlite = "sqlite"
    mssql = "mssql"


def run(dialect: Dialect, path: Path, skip_errors: bool = False) -> Type[DeclarativeBase]:
    base = get_declarative_base(path, skip_errors)
    return dump_ddl(dialect.value, base)


@app.command()
def load(dialect: Dialect = Dialect.mysql,
         path: Path = typer.Option(exists=True, help="Path to directory of the sqlalchemy models."),
         skip_errors: bool = typer.Option(False, help="Skip errors when loading models.")
         ):
    if path is None:
        path = Path(os.getcwd())
    run(dialect, path, skip_errors)


if __name__ == "__main__":
    app(prog_name='atlas-provider-sqlalchemy')
