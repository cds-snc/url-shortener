terraform {
  source = "../../../aws//security_hub"
}

include {
  path = find_in_parent_folders()
}
