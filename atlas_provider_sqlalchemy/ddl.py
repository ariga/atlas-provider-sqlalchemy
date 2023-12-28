import os
import importlib.util
import inspect
from pathlib import Path
from sqlalchemy import create_mock_engine
from sqlalchemy.orm import DeclarativeBase
from typing import Type, Set, List


class ModelsNotFoundError(Exception):
    pass


def get_declarative_base(models_dir: Path, debug: bool = False) -> Type[DeclarativeBase]:
    """
    Walk the directory tree starting at the root, import all models, and return 1 of them, as they all keep a
    reference to the Metadata object. The way sqlalchemy works, you must import all classes in order for them to be
    registered in Metadata.
    """

    models: Set[Type[DeclarativeBase]] = set()
    for root, _, _ in os.walk(models_dir):
        python_file_paths = Path(root).glob('*.py')
        for file_path in python_file_paths:
            try:
                module_spec = importlib.util.spec_from_file_location(
                    file_path.stem, file_path)
                if module_spec and module_spec.loader:
                    module = importlib.util.module_from_spec(module_spec)
                    module_spec.loader.exec_module(module)
            except Exception as e:
                if debug:
                    print(f'{e.__class__.__name__}: {str(e)}')
                # TODO: handle nicer
                continue
            classes = {c[1]
                       for c in inspect.getmembers(module, inspect.isclass)
                       if issubclass(c[1], DeclarativeBase) and c[1] is not DeclarativeBase}
            models.update(classes)
    try:
        model = models.pop()
    except KeyError:
        raise ModelsNotFoundError(
            'Found no sqlalchemy models in the directory tree.')
    return model


def dump_ddl(dialect_driver: str, base: Type[DeclarativeBase]) -> Type[DeclarativeBase]:
    """
    Creates a mock engine and dumps its DDL to stdout
    """

    def dump(sql, *multiparams, **params):
        print(str(sql.compile(dialect=engine.dialect)).replace('\t', '').replace('\n', ''), end=';\n\n')

    engine = create_mock_engine(f'{dialect_driver}://', dump)
    base.metadata.create_all(engine, checkfirst=False)
    return base


def get_import_path_from_path(path: Path, root_dir: Path) -> str:
    import_path = '.'.join(path.relative_to(
        root_dir).parts).replace(path.suffix, '')
    return import_path


def print_ddl(dialect_driver: str, models: List[Type[DeclarativeBase]]):
    dump_ddl(dialect_driver=dialect_driver, base=models[0])
