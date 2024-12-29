import os
import sys
from enum import Enum
from pathlib import Path

import typer
from sqlalchemy import MetaData

from atlas_provider_sqlalchemy.ddl import (
    ModuleImportError,
    ModelsNotFoundError,
    dump_ddl,
    get_metadata,
)

app = typer.Typer(no_args_is_help=True)


class Dialect(str, Enum):
    mysql = "mysql"
    mariadb = "mariadb"
    postgresql = "postgresql"
    sqlite = "sqlite"
    mssql = "mssql"


def run(dialect: Dialect, path: Path, skip_errors: bool = False) -> MetaData:
    metadata = get_metadata(path, skip_errors)
    return dump_ddl(dialect.value, metadata)


@app.command()
def load(dialect: Dialect = Dialect.mysql,
         path: Path = typer.Option(exists=True, help="Path to directory of the sqlalchemy models."),
         skip_errors: bool = typer.Option(False, help="Skip errors when loading models.")
         ):
    if path is None:
        path = Path(os.getcwd())
    try:
        run(dialect, path, skip_errors)
    except ModuleImportError as e:
        print(e, file=sys.stderr)
        print("To skip on failed import, run: atlas-provider-sqlalchemy --skip-errors", file=sys.stderr)
        exit(1)
    except ModelsNotFoundError as e:
        print(e, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    app(prog_name="atlas-provider-sqlalchemy")
