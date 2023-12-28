import os
from pathlib import Path
from typing import Optional
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


def run(dialect: Dialect, path: Path, debug: bool = False) -> Type[DeclarativeBase]:
    base = get_declarative_base(path, debug)
    return dump_ddl(dialect.value, base)


@app.command()
def load(dialect: Dialect = Dialect.mysql,
         path: Optional[Path] = typer.Option(None, exists=True, help="Path to directory of the sqlalchemy models."),
         debug: bool = False):
    if path is None:
        path = Path(os.getcwd())
    run(dialect, path, debug)


if __name__ == "__main__":
    app(prog_name='atlas-provider-sqlalchemy')
