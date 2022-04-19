terraform {
  source = "../../aws//hosted_zone"
}

inputs = {
  hosted_zone_name = "url-shortener.cdssandbox.xyz"
}

include {
  path = find_in_parent_folders()
}
