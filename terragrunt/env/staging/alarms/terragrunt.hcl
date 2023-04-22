terraform {
  source = "../../../aws//alarms"
}

dependencies {
  paths = ["../api"]
}

dependency "api" {
  config_path = "../api"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    function_name = "/aws/lambda/url-shortener-api"
  }
}

inputs = {
  function_name                     = dependency.api.outputs.function_name
  api_error_threshold                = "1"
  api_suspicious_threshold           = "5"
  api_warning_threshold              = "10"
}

include {
  path = find_in_parent_folders()
}
