variable "api_auth_token" {
	type = string
	sensitive = true
}

variable "rds_username" {
	type = string
}

variable "rds_password" {
	type = string
	sensitive = true
}

variable "domain_name" {
  type = string
}

variable "hosted_zone_id" {
  type = string
}
