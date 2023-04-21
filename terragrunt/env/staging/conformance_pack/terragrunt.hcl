terraform {
  source = "../../../aws//conformance_pack"
}

dependencies {
  paths = ["../network"]
}

dependency "network" {
  config_path = "../network"

  mock_outputs_allowed_terraform_commands = ["init", "fmt", "validate", "plan", "show"]
  mock_outputs_merge_with_state           = true
  mock_outputs = {
    vpc_id = "url_shortener_vpc_id"
  }
}

inputs = {
  vpc_id	 = dependency.network.outputs.vpc_id
}  

include {
  path = find_in_parent_folders()
}
