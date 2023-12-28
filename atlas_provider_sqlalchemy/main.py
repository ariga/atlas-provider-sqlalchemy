import os
from pathlib import Path
import typer
from sqlalchemy.orm import DeclarativeBase
from typing import Type
from atlas_provider_sqlalchemy.ddl import get_declarative_base, dump_ddl

app = typer.Typer(no_args_is_help=True)


def run(dialect: str, modles_dir: str = '', debug: bool = False) -> Type[DeclarativeBase]:
    models_dir = Path(modles_dir) or Path(os.getcwd())
    base = get_declarative_base(models_dir, debug)
    return dump_ddl(dialect, base)


@app.command()
def load(dialect: str = typer.Option(default=...), path: str = '', debug: bool = False):
    run(dialect, path, debug)


if __name__ == "__main__":
    app(prog_name='atlas-provider-sqlalchemy')
