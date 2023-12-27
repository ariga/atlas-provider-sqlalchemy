variable "dialect" {
  type = string
}

locals {
  dev_url = {
    mysql = "docker://mysql/8/dev"
    postgresql = "docker://postgres/15"
    sqlite = "sqlite://file::memory:?cache=shared"
  }[var.dialect]
}

data "external_schema" "sqlalchemy" {
  program = [
    "poetry",
    "run",
    "python3",
    "load_models.py",
    var.dialect, // mysql | postgresql | sqlite | mssql+pyodbc
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