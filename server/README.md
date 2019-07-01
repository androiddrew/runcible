# Runcible

A development  API to be used in vuejs courses and tutorials.

## Configuration

The application relies on a settings.toml file located in application's top level directory. Contents should

```
[common]
database_engine_dsn = "postgresql://runcible:@localhost/runcible"

[dev]
database_engine_params.echo = true
database_engine_params.connect_args.options = "-c timezone=utc"
CORS_HEADERS = "*"
CORS_METHODS = "*"
CORS_ORIGIN = "*"
CORS_MAXAGE = "86400"

[test]
database_engine_dsn = "<YOUR SQLALCHEMY TEST DB CONNECTION STRING HERE>"
database_engine_params.echo = true


```

Use the environmental variable `ENVIRONMENT` to switch between configurations. Defaults to `dev`.
