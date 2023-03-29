terraform {
  source = "../../../aws//backup_plan"
}

dependencies {
  paths = ["../dynamodb"]
}

dependency "dynamodb" {
  config_path = "../dynamodb"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_with_state           = true
  mock_outputs = {
    url_shortener_table_arn = ""
  }
}

inputs = {
  url_shortener_table_arn = dependency.dynamodb.outputs.url_shortener_table_arn
  }

include {
  path = find_in_parent_folders()
}
