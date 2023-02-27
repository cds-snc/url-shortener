terraform {
    source = "git::https://github.com/cds-snc/scan-files//terragrunt/aws/alarms?ref=${get_env("INFRASTRUCTURE_VERSION")}"
}

dependencies {
  paths = ["../api"]
}

dependency "api" {
  config_path = "../api"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    function_log_group_name        = "/aws/lambda/url-shortener-api"
  }
}

inputs = {
  url_shortener_api_log_group_name  = dependency.api.outputs.function_log_group_name

  api_error_threshold                = "1"
  api_warning_threshold              = "5"
}

include {
  path = find_in_parent_folders()
}
