# atlas-provider-sqlalchemy

Use [Atlas](https://atlasgo.io/) with [SQLAlchemy](https://www.sqlalchemy.org/) to manage your database schema as code. By connecting your SQLAlchemy models to Atlas,
you can define and edit your schema directly in Python, and Atlas will automatically plan and apply database schema migrations for you, eliminating
the need to write migrations manually.

Atlas brings automated CI/CD workflows to your database, along with built-in support for [testing](https://atlasgo.io/testing/schema), [linting](https://atlasgo.io/versioned/lint),
schema [drift detection](https://atlasgo.io/monitoring/drift-detection), and [schema monitoring](https://atlasgo.io/monitoring). It also allows you to extend SQLAlchemy with
advanced database objects such as triggers, row-level security, and custom functions that are not supported natively.

### Use-cases
1. [**Declarative migrations**](https://atlasgo.io/declarative/apply) - Use the Terraform-like `atlas schema apply --env sqlalchemy` command to apply your SQLAlchemy schema to the database.
2. [**Automatic migration planning**](https://atlasgo.io/versioned/diff) - Use `atlas migrate diff --env sqlalchemy` to automatically plan database schema changes and generate
   a migration from the current database version to the desired version defined by your SQLAlchemy schema.

### Installation

Install Atlas from macOS or Linux by running:
```bash
curl -sSf https://atlasgo.sh | sh
```

See [atlasgo.io](https://atlasgo.io/getting-started#installation) for more installation options.

Install the provider by running:
```bash
# The Provider works by importing your SQLAlchemy models and extracting the schema from them.
# Therefore, you will need to run the provider from within your project's Python environment.
pip install atlas-provider-sqlalchemy
```

#### Standalone 

If all of your SQLAlchemy models exist in a single package, 
you can use the provider directly to load your SQLAlchemy schema into Atlas.

In your project directory, create a new file named `atlas.hcl` with the following contents:

```hcl
data "external_schema" "sqlalchemy" {
  program = [
    "atlas-provider-sqlalchemy",
    "--path", "./path/to/models",
    "--dialect", "mysql" // mariadb | postgresql | sqlite | mssql
  ]
}

env "sqlalchemy" {
  src = data.external_schema.sqlalchemy.url
  dev = "docker://mysql/8/dev"
  migration {
    dir = "file://migrations"
  }
  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}
```

#### As Python Script 

If you want to use the provider as a python script, you can use the provider as follows:

Create a new file named `load_models.py` with the following contents:

```python
# import all models
from models import User, Task
from atlas_provider_sqlalchemy.ddl import print_ddl
print_ddl("mysql", [User, Task])
```

Next, in your project directory, create a new file named `atlas.hcl` with the following contents:

```hcl
data "external_schema" "sqlalchemy" {
    program = [
        "python",
        "load_models.py"
    ]
}

env "sqlalchemy" {
  src = data.external_schema.sqlalchemy.url
  dev = "docker://mysql/8/dev"
  migration {
    dir = "file://migrations"
  }
  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}
```

### Usage

Once you have the provider installed, you can use it to apply your SQLAlchemy schema to the database:

#### Apply

You can use the `atlas schema apply` command to plan and apply a migration of your database to your current SQLAlchemy schema.
This works by inspecting the target database and comparing it to the SQLAlchemy schema and creating a migration plan.
Atlas will prompt you to confirm the migration plan before applying it to the database.

```bash
atlas schema apply --env sqlalchemy -u "mysql://root:password@localhost:3306/mydb"
```
Where the `-u` flag accepts the [URL](https://atlasgo.io/concepts/url) to the
target database.

#### Diff

Atlas supports a [version migration](https://atlasgo.io/concepts/declarative-vs-versioned#versioned-migrations) 
workflow, where each change to the database is versioned and recorded in a migration file. You can use the
`atlas migrate diff` command to automatically generate a migration file that will migrate the database
from its latest revision to the current SQLAlchemy schema.

```bash
atlas migrate diff --env sqlalchemy 
````

### Supported Databases

The provider supports the following databases:
* MySQL
* MariaDB
* PostgreSQL
* SQLite
* Microsoft SQL Server
* ClickHouse

### FAQ

#### How to include schema creation in the migration?

Sometimes your tables may not reside in the default schema, and you may want to create the schema as part of the migration.

you can utilize [composite schemas](https://atlasgo.io/atlas-schema/projects#data-source-composite_schema) to add custom DDL in addition to the SQLAlchemy schema.

change your `atlas.hcl` like this:

```hcl

data "external_schema" "sqlalchemy" {
  program = [
    "atlas-provider-sqlalchemy",
    "--path", "./path/to/models",
    "--dialect", "postgresql"
  ]
}

data "composite_schema" "app" {
    # Create the test schema first
    schema "public" {
        url = "file://schema.sql"
    }
   # Next, load the sqlalchemy models.
    schema "public" {
        url = data.external_schema.sqlalchemy.url
    }
}

env "sqlalchemy" {
  src = data.composite_schema.app.url
  dev = "docker://postgres/16/dev"
  migration {
    dir = "file://migrations"
  }
  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}
```

and create a `schema.sql` file with the following contents (change the schema name as needed):

```sql
CREATE SCHEMA IF NOT EXISTS test;
```

### Credit

The code in this repository is based on [noamtamir/atlas-provider-sqlalchemy](https://github.com/noamtamir/atlas-provider-sqlalchemy).

### Issues

Please report any issues or feature requests in the [ariga/atlas](https://github.com/ariga/atlas/issues) repository.

### License

This project is licensed under the [Apache License 2.0](LICENSE).
