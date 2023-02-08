terraform {
  source = "git::https://github.com/cds-snc/url-shortener//terragrunt/aws/network?ref=${get_env("INFRASTRUCTURE_VERSION")}"
}

include {
  path = find_in_parent_folders()
