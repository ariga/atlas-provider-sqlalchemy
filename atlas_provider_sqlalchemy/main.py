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
    get_file_directives,
)

app = typer.Typer(no_args_is_help=True)


class Dialect(str, Enum):
    mysql = "mysql"
    mariadb = "mariadb"
    postgresql = "postgresql"
    sqlite = "sqlite"
    mssql = "mssql"
    clickhouse = "clickhouse"


def run(
    dialect: Dialect, path: list[Path], skip_errors: bool = False
) -> list[MetaData]:
    metadata_list: list[MetaData] = []
    directives = []
    for p in path:
        m = get_metadata(p, skip_errors)
        metadata_list.append(m)
        directives.extend(get_file_directives(p, m))
    dump_ddl(dialect.value, metadata_list, directives)
    return metadata_list


@app.command()
def load(
    dialect: Dialect = Dialect.mysql,
    path: list[Path] = typer.Option(
        exists=True, help="Path to directory of the sqlalchemy models."
    ),
    skip_errors: bool = typer.Option(False, help="Skip errors when loading models."),
):
    if not path:
        path = [Path(os.getcwd())]
    try:
        run(dialect, path, skip_errors)
    except ModuleImportError as e:
        print(e, file=sys.stderr)
        print(
            "To skip on failed import, run: atlas-provider-sqlalchemy --skip-errors",
            file=sys.stderr,
        )
        exit(1)
    except ModelsNotFoundError as e:
        print(e, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    app(prog_name="atlas-provider-sqlalchemy")
