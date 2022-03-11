terraform {
  source = "../../aws//hosted_zone"
}

inputs = {
  hosted_zone_name = ""
}

include {
  path = find_in_parent_folders()
}
