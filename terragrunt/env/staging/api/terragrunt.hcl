terraform {
  source = "../../../aws//api"
}

dependencies {
  paths = ["../network", "../ecr"]
}

dependency "network" {
  config_path = "../network"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_with_state           = true
  mock_outputs = {
    api_id = ""
    private_subnet_ids                  = [""]
  }
}

dependency "ecr" {
  config_path = "../ecr"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_with_state           = true
  mock_outputs = {
    ecr_repository_arn = ""
    ecr_repository_url = ""
    apache_repository_arn = ""
    apache_repository_url = ""
  }
}

include {
  path = find_in_parent_folders()
}
