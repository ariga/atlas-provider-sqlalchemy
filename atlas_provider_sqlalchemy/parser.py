"""Parse SQLAlchemy models using native ast  to extract line number information.

This module provides utilities to locate tables, columns, and other SQL
elements in SQLAlchemy model definitions using source code analysis.
"""

from typing import Dict, Optional, Tuple, Any
import ast

class SQLAlchemyModelVisitor(ast.NodeVisitor):
    """Visit AST nodes to find SQLAlchemy model definitions."""

    def __init__(self):
        super().__init__()
        # Store table information: {table_name: (line_number, class_node)}
        self.tables: Dict[str, Tuple[int, Any]] = {}
        # Current table being visited
        self.current_table: Optional[str] = None

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit a class definition and check if it's a SQLAlchemy model."""
        line_number = node.lineno
        
        # Check for __tablename__ attribute in the class body
        for statement in node.body:
            if isinstance(statement, ast.Assign) and len(statement.targets) == 1:
                target = statement.targets[0]
                if isinstance(target, ast.Name) and target.id == "__tablename__":
                    if isinstance(statement.value, ast.Str):
                        table_name = statement.value.s
                        self.tables[table_name] = (line_number, node)
                        break
        
        # Continue visiting child nodes
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        """Visit assignment nodes to find SQLAlchemy Table definitions."""
        # Check if this is a direct Table definition
        if isinstance(node.value, ast.Call):
            func = node.value.func
            is_table_call = False
            if isinstance(func, ast.Attribute) and func.attr == "Table":
                is_table_call = True
            if is_table_call and node.value.args:
                first_arg = node.value.args[0]
                if isinstance(first_arg, ast.Str):
                    table_name = first_arg.s
                    self.tables[table_name] = (node.lineno, node)
        
        # Continue visiting child nodes
        self.generic_visit(node)

def parse_file(file_path: str) -> SQLAlchemyModelVisitor:
    """Parse a Python file and extract SQLAlchemy model information.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        SQLAlchemyModelVisitor: A visitor instance containing found tables and columns.
        
    Raises:
        FileNotFoundError: If the file cannot be found
        Exception: If there are parsing errors
    """
    try:
        with open(file_path, 'r') as f:
            source_code = f.read()
        
        # Parse the source code with ast
        module = ast.parse(source_code, filename=file_path)
        visitor = SQLAlchemyModelVisitor()
        visitor.visit(module)
        
        return visitor
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find file: {file_path}")
    except Exception as e:
        raise Exception(f"Error parsing file {file_path}: {str(e)}")
