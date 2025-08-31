variable "dialect" {
  type = string
}

variable "path" {
  type = string
  default = "testdata/models"
}

locals {
  dev_url = {
    mysql = "docker://mysql/8/dev"
    postgresql = "docker://postgres/15"
    sqlite = "sqlite://?mode=memory&_fk=1"
    mssql = "docker://sqlserver/2022-latest"
  }[var.dialect]
}

data "external_schema" "sqlalchemy" {
  program = [
    "poetry",
    "run",
    "python3",
    "../atlas_provider_sqlalchemy/main.py",
    "--path", var.path,
    "--dialect", var.dialect, // mysql | postgresql | sqlite | mssql
  ]
}

env "sqlalchemy" {
  src = data.external_schema.sqlalchemy.url
  dev = local.dev_url
  migration {
    dir = "file://migrations/${var.dialect}"
  }
  diff {
    skip {
      rename_constraint = true
    }
  }
  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}
