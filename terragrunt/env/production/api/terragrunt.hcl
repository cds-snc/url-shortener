terraform {
  source = "../../../aws//api"
}

inputs = {
  oidc_exists    = true
}

include {
  path = find_in_parent_folders()
}
