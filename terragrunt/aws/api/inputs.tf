variable "api_auth_token" {
  description = "The API token needed for all requests to the API."
  type        = string
  sensitive   = true
}

variable "hashing_peppers" {
  description = "csv of peppers used by hashing algorithm."
  type        = string
  sensitive   = true
}

variable "url_shortener_table_name" {
  description = "DynamoDB table name for the URL shortener"
  type        = string
}

variable "ecr_repository_arn" {
  description = "Arn of the ECR Repository"
  type        = string
}

variable "ecr_repository_url" {
  description = "URL of the URL shortener ECR"
  type        = string
}

variable "api_security_group_id" {
  description = "Api security group Id"
  type        = string
}

variable "private_subnet_ids" {
  description = "List of the URL Shortner VPC private subnet ids"
  type        = list(string)
}

variable "ecr_tag" {
  description = "The tag used for the ECR to specifiy either a specific version or latest"
  type        = string
}
