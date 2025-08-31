"""
Test case for GitHub issue #16: "Sometimes atlas-provider-sqlalchemy outputs nothing"

This test verifies that the fix for module caching issues works correctly,
particularly the scenario where file content changes (like after git branch switches)
but Python's bytecode cache might return stale data.
"""

import tempfile
import time
from pathlib import Path

from atlas_provider_sqlalchemy.ddl import get_metadata


def create_sqlalchemy_model_file(
    file_path: Path, table_name: str, class_name: str = "TestModel"
):
    """Create a SQLAlchemy model file with the given table name"""
    content = f'''
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class {class_name}(Base):
    __tablename__ = "{table_name}"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
'''
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)


def test_module_caching_fix():
    """Test that the module caching fix works correctly.

    This test reproduces the scenario where:
    1. A file is loaded and processed
    2. The same file is modified (simulating git branch switch)
    3. The file is loaded again and should reflect the changes

    Without the fix, step 3 would return stale cached data.
    With the fix, step 3 should return the updated data.
    """

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        models_dir = temp_path / "models"
        models_file = models_dir / "models.py"

        # Step 1: Create initial model file
        create_sqlalchemy_model_file(models_file, "initial_table", "InitialModel")

        # Load metadata - should find the initial table
        metadata1 = get_metadata(models_dir)
        assert "initial_table" in metadata1.tables
        assert len(metadata1.tables) == 1

        # Step 2: Modify the file (simulate git branch switch)
        # Wait a moment to ensure different modification time
        time.sleep(0.1)
        # Use a completely different class name and structure to avoid SQLAlchemy caching issues
        modified_content = """
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class CompletelyDifferentModel(Base):
    __tablename__ = "changed_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(100))
"""
        models_file.write_text(modified_content)

        # Step 3: Load metadata again - should find the changed table
        metadata2 = get_metadata(models_dir)

        # The fix should ensure we get the updated content
        # If this fails, it means caching is still an issue
        try:
            assert "changed_table" in metadata2.tables
            assert "initial_table" not in metadata2.tables
            assert len(metadata2.tables) == 1
        except AssertionError:
            # Print debug info if assertion fails
            print(f"Expected 'changed_table', got: {list(metadata2.tables.keys())}")
            print(f"File modification time: {models_file.stat().st_mtime}")
            print(f"File content: {models_file.read_text()[:200]}...")
            raise

        # Verify the metadata objects are different (not cached)
        assert metadata1 is not metadata2


def test_multiple_files_with_same_stem():
    """Test that files with the same stem name don't interfere with each other.

    This tests the scenario where multiple directories contain files with
    the same name (e.g., models.py), which was part of the original caching issue.
    """

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create two subdirectories with files having the same name
        dir1 = temp_path / "app1"
        dir2 = temp_path / "app2"

        file1 = dir1 / "models.py"
        file2 = dir2 / "models.py"

        create_sqlalchemy_model_file(file1, "table1", "Model1")
        create_sqlalchemy_model_file(file2, "table2", "Model2")

        # Load metadata from each directory separately
        metadata1 = get_metadata(dir1)
        metadata2 = get_metadata(dir2)

        # Verify each directory loads its own tables correctly
        assert "table1" in metadata1.tables
        assert "table1" not in metadata2.tables

        assert "table2" in metadata2.tables
        assert "table2" not in metadata1.tables

        # Verify the metadata objects are different
        assert metadata1 is not metadata2


def test_file_modification_time_tracking():
    """Test that the fix properly tracks file modification times.

    This ensures that the unique module naming includes file modification time,
    which is crucial for detecting when files have changed.
    """

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        models_dir = temp_path / "models"
        models_file = models_dir / "models.py"

        # Create initial file
        create_sqlalchemy_model_file(models_file, "table_v1", "ModelV1")
        initial_mtime = models_file.stat().st_mtime

        # Load metadata
        metadata1 = get_metadata(models_dir)
        assert "table_v1" in metadata1.tables

        # Wait and modify file to ensure different mtime
        time.sleep(0.1)
        # Use a completely different structure to ensure change is detected
        new_content = """
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Integer

class Base(DeclarativeBase):
    pass

class ModelV2(Base):
    __tablename__ = "table_v2"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    version: Mapped[int] = mapped_column(Integer())
"""
        models_file.write_text(new_content)
        new_mtime = models_file.stat().st_mtime

        # Verify mtime actually changed
        assert new_mtime > initial_mtime

        # Load metadata again - should reflect the changes
        metadata2 = get_metadata(models_dir)

        try:
            assert "table_v2" in metadata2.tables
            assert "table_v1" not in metadata2.tables
        except AssertionError:
            # Print debug info if assertion fails
            print(f"Expected 'table_v2', got: {list(metadata2.tables.keys())}")
            print(f"Initial mtime: {initial_mtime}, New mtime: {new_mtime}")
            print(f"File content: {models_file.read_text()[:200]}...")
            raise
