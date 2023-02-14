terraform {
  source = "../../../aws//cloudfront"
}

dependencies {
  paths = ["../hosted_zone", "../network", "../api"]
}

dependency "hosted_zone" {
  config_path = "../hosted_zone"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_with_state           = true
  mock_outputs = {
    hosted_zone_id = "1234567890"
  }
}

dependency "network" {
  config_path = "../network"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_with_state           = true
  mock_outputs = {
    vpc_id = "url_shortener_vpc_id"
  }
}

dependency "api" {
  config_path = "../api"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_with_state           = true
  mock_outputs = {
    function_name = "url-shortener-api"
    function_url  = "https://api.url_shortener_url.com"
  }
}

inputs = {
  hosted_zone_id = dependency.hosted_zone.outputs.hosted_zone_id
  function_name  = dependency.api.outputs.function_name
  function_url   = dependency.api.outputs.function_url
  vpc_id	 = dependency.network.outputs.vpc_id
}  

include {
  path = find_in_parent_folders()
}
