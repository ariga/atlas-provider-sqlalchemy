import sys

from cli.main import print_ddl
from tests.models.models import User, Address

# get the dialect from the command line
dialect = sys.argv[1]

print_ddl(dialect, [User, Address])
