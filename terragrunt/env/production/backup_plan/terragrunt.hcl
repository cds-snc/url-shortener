terraform {
  source="git::https://github.com/cds-snc/url-shortener//terragrunt/aws/backup_plan?ref=${get_env("INFRASTRUCTURE_VERSION")}"
}

dependencies {
  paths = ["../dynamodb"]
}

dependency "dynamodb" {
  config_path = "../dynamodb"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_with_state           = true
  mock_outputs = {
    url_shortener_table_arn = "arn:aws:dynamodb:ca-central-1:123456789012:table/url_shortener"
  }
}

inputs = {
  url_shortener_table_arn = dependency.dynamodb.outputs.url_shortener_table_arn
  }

include {
  path = find_in_parent_folders()
}
