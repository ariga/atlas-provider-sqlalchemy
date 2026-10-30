# Importing by module name gives FirstBase a second copy with the same tables.
from tests.testdata.multi_base.users import User

__all__ = ["User"]
