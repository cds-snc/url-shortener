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
    api_security_group_id = ""
    private_subnet_ids = [""]
  }
}

dependency "ecr" {
  config_path = "../ecr"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_with_state           = true
  mock_outputs = {
    ecr_repository_arn = ""
    ecr_repository_url = ""
  }
}

inputs = {
  api_security_group_id = dependency.network.outputs.api_security_group_id
  private_subnet_ids	= dependency.network.outputs.private_subnet_ids
  ecr_repository_arn	= dependency.ecr.outputs.ecr_repository_arn
  ecr_repository_url	= dependency.ecr.outputs.ecr_repository_url
  ecr_tag		= "latest"
  url_shortener_table_name = "url_shortener_table"
  }  

include {
  path = find_in_parent_folders()
}
