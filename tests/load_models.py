import sys

from atlas_provider_sqlalchemy.ddl import print_ddl
from tests.testdata.models.models import User, Address

# get the dialect from the command line
dialect = sys.argv[1]

print_ddl(dialect, [User, Address])
