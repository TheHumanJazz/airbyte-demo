terraform {
  required_providers {
    airbyte = {
      source  = "airbytehq/airbyte"
      version = "~> 1.0"
    }
  }
}

provider "airbyte" {
  # client_id     = var.client_id
  # client_secret = var.client_secret

  server_url = "http://airbyte.localtest.me/api/public/v1/"
}

data "airbyte_connector_configuration" "postgres_config" {
  connector_name = "source-postgres"

  configuration = {
    host     = "localhost"
    port     = 5432
    database = "postgres"
    username = "postgres"
  }

  configuration_secrets = {
    password = "postgres"
  }
}

resource "airbyte_source" "postgres" {
  name          = "Jared Test Postgres"
  workspace_id  = "615afe89-5923-4ba3-9dd6-fbe00c20d310"
  definition_id = data.airbyte_connector_configuration.postgres_config.definition_id
  configuration = data.airbyte_connector_configuration.postgres_config.configuration_json
}
