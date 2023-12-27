data "external_schema" "sqlalchemy" {
  program = [
    "atlas-provider-sqlalchemy",
    "--dialect", "mysql", // mysql | mariadb | postgresql | sqlite | mssql
  ]
}

env "sqlalchemy" {
  src = data.external_schema.sqlalchemy.url
  dev = "docker://mysql/8/dev"
}