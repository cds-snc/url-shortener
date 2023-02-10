terraform {
  source = "../../../aws//network"
}

include {
  path = find_in_parent_folders()
}
