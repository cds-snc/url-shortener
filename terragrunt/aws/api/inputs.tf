variable "auth_token_app" {
  description = "The authorization bearer token needed for requests to the API from the app itself."
  type        = string
  sensitive   = true
}

variable "auth_token_notify" {
  description = "The authorization bearer token needed for requests to the API from Notify."
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

variable "notify_api_key" {
  description = "The API key used to send emails via Notify"
  type        = string
  sensitive   = true
}

variable "notify_contact_email" {
  description = "The email address used by Notify to send contact form emails to"
  type        = string
  sensitive   = true
}

variable "shortener_path_length" {
  description = "A variable to set the length of the shortened url"
  type        = string
  default     = "8"
}