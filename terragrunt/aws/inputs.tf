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
