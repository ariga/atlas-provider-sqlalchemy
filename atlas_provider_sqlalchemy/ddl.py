import os
import importlib.util
import inspect
from pathlib import Path
from typing import Any, Protocol
from atlas_provider_sqlalchemy import parser

import sqlalchemy as sa

class DBTableDesc(Protocol):
    """Database table description (SQLAlchemy table or model)."""

    metadata: sa.MetaData


class ModuleImportError(Exception):
    pass


class ModelsNotFoundError(Exception):
    pass


def sqlalchemy_version() -> tuple[int, ...]:
    """Get major and minor version of sqlalchemy."""

    return tuple(int(x) for x in sa.__version__.split("."))


def create_mock_engine(url: str, executor: Any) -> Any:
    """Create a "mock" engine used for echoing DDL."""

    if sqlalchemy_version() < (1, 4):
        return sa.create_engine(url, strategy="mock", executor=executor)
    else:
        return sa.create_mock_engine(url, executor)


def get_metadata(db_dir: Path, skip_errors: bool = False) -> sa.MetaData:
    """Walk the directory tree starting at the root, import all models and
    tables, and return metadata for one of them, as they all keep a reference
    to the `MetaData` object.  The way SQLAlchemy works, you must import all
    models and tables in order for them to be registered in metadata.
    """

    metadata: set[sa.MetaData] = set()

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
                if hasattr(v, "metadata") and isinstance(v.metadata, sa.MetaData)
            }
            metadata.update(ms)

    if not metadata:
        raise ModelsNotFoundError("Found no sqlalchemy models/tables in the directory tree.")

    return metadata.pop()

def get_metadata_file(file: Path) -> sa.MetaData:
    """Get metadata from a single file."""

    if not file.is_file() or not file.suffix == ".py":
        raise ModelsNotFoundError(f"File {file} is not a valid Python file.")

    try:
        module_spec = importlib.util.spec_from_file_location(file.stem, file)
        if module_spec and module_spec.loader:
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
    except Exception as e:
        raise ModuleImportError(f"{e.__class__.__name__}: {str(e)} in {file}")

    metadata = {
        v.metadata
        for (_, v) in inspect.getmembers(module)
        if hasattr(v, "metadata") and isinstance(v.metadata, sa.MetaData)
    }

    if not metadata:
        raise ModelsNotFoundError(f"No sqlalchemy models/tables found in {file}.")

    return metadata.pop()

def get_file_directives(db_dir: Path) -> list[str]:
    """Get all file directives from the given directory."""
    directives = []
    for root, _, files in os.walk(db_dir):
        for file in files:
            if file.endswith(".py"):
                # Parse the file for directives
                file_path = Path(root) / file
                abs_file_path = file_path.absolute()
                visitor = parser.parse_file(file_path)
                metadata = get_metadata_file(file_path)
                # Extract table directives
                if visitor.tables:
                    for table_name, (line_number, _ ) in visitor.tables.items():
                        # If table_name is not in metadata, skip it
                        if table_name not in metadata.tables:
                            continue
                        directive = f"atlas:pos {table_name}[type=table] {abs_file_path}:{line_number}"
                        directives.append(directive)
    return directives


def dump_ddl(dialect_driver: str, metadata: sa.MetaData, directives: [str]) -> sa.MetaData:
    """Dump DDL statements for the given metadata to stdout."""
    def dump(sql, *multiparams, **params):
        print(str(sql.compile(dialect=engine.dialect)).replace("\t", "").replace("\n", ""), end=";\n\n")

    """Add File directives to the DDL dump."""
    if directives:
        for directive in directives:
            print(f"-- {directive}")
        print()
    engine = create_mock_engine(f"{dialect_driver}://", dump)
    metadata.create_all(engine, checkfirst=False)
    return metadata


def print_ddl(dialect_driver: str, models: list[DBTableDesc]) -> None:
    """Dump DDL statements for the metadata from the given models/tables to stdout."""
    dump_ddl(dialect_driver=dialect_driver, metadata=models[0].metadata, directives=[])
