import os
import importlib.util
import inspect
from pathlib import Path
from typing import Protocol

from sqlalchemy import MetaData, create_mock_engine


class DBTableDesc(Protocol):
    """Database table description (SQLAlchemy table or model)."""

    metadata: MetaData


class ModuleImportError(Exception):
    pass


class ModelsNotFoundError(Exception):
    pass


def get_metadata(db_dir: Path, skip_errors: bool = False) -> MetaData:
    """Walk the directory tree starting at the root, import all models and
    tables, and return metadata for one of them, as they all keep a reference
    to the `MetaData` object.  The way SQLAlchemy works, you must import all
    models and tables in order for them to be registered in metadata.
    """

    metadata: set[MetaData] = set()

    for root, _, _ in os.walk(db_dir):
        python_file_paths = Path(root).glob("*.py")
        for file_path in python_file_paths:
            try:
                module_spec = importlib.util.spec_from_file_location(
                    file_path.stem,
                    file_path,
                )
                if module_spec and module_spec.loader:
                    module = importlib.util.module_from_spec(module_spec)
                    module_spec.loader.exec_module(module)
            except Exception as e:
                if skip_errors:
                    continue

                raise ModuleImportError(f"{e.__class__.__name__}: {str(e)} in {file_path}")

            ms = {
                v.metadata
                for (_, v) in inspect.getmembers(module)
                if hasattr(v, "metadata") and isinstance(v.metadata, MetaData)
            }
            metadata.update(ms)

    if not metadata:
        raise ModelsNotFoundError("Found no sqlalchemy models/tables in the directory tree.")

    return metadata.pop()


def dump_ddl(dialect_driver: str, metadata: MetaData) -> MetaData:
    """Dump DDL statements for the given metadata to stdout."""

    def dump(sql, *multiparams, **params):
        print(str(sql.compile(dialect=engine.dialect)).replace("\t", "").replace("\n", ""), end=";\n\n")

    engine = create_mock_engine(f"{dialect_driver}://", dump)
    metadata.create_all(engine, checkfirst=False)
    return metadata


def print_ddl(dialect_driver: str, models: list[DBTableDesc]) -> None:
    """Dump DDL statements for the metadata from the given models/tables to stdout."""

    dump_ddl(dialect_driver=dialect_driver, metadata=models[0].metadata)
