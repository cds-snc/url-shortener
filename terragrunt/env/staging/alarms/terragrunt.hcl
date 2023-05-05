terraform {
  source = "../../../aws//alarms"
}

dependencies {
  paths = ["../hosted_zone", "../api", "../cloudfront"]
}

dependency "hosted_zone" {
  config_path = "../hosted_zone"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    hosted_zone_id = "Z00123456I4SMQMHD8PKB"
  }
}

dependency "api" {
  config_path = "../api"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    function_name = "/aws/lambda/url-shortener-api"
  }
}

dependency "cloudfront" {
  config_path = "../cloudfront"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_strategy_with_state  = "shallow"
  mock_outputs = {
    cloudfront_api_arn = "arn:aws:cloudfront::123456789012:distribution/A2Z6W4OZAEKEKP"
  }
}

inputs = {
  api_error_threshold                = "1"
  api_high_magic_link_sent_threshold = "10"
  api_suspicious_threshold           = "5"
  api_warning_threshold              = "10"
  cloudfront_api_arn                 = dependency.cloudfront.outputs.cloudfront_api_arn
  function_name                      = dependency.api.outputs.function_name
  hosted_zone_id                     = dependency.hosted_zone.outputs.hosted_zone_id
}

include {
  path = find_in_parent_folders()
}
