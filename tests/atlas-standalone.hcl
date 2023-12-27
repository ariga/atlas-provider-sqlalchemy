variable "dialect" {
  type = string
}

locals {
  dev_url = {
    mysql = "docker://mysql/8/dev"
    postgresql = "docker://postgres/15"
    sqlite = "sqlite://?mode=memory&_fk=1"
  }[var.dialect]
}

data "external_schema" "sqlalchemy" {
  program = [
    "poetry",
    "run",
    "python3",
    "../atlas_provider_sqlalchemy/main.py",
    "--path", "models",
    "--dialect", var.dialect, // mysql | postgresql | sqlite | mssql+pyodbc
  ]
}

env "sqlalchemy" {
  src = data.external_schema.sqlalchemy.url
  dev = local.dev_url
  migration {
    dir = "file://migrations/${var.dialect}"
  }
  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}
