variable "api_auth_token" {
  description = "The API token needed for all requests to the API."
  type        = string
  sensitive   = true
}

variable "url_shortener_table_name" {
  description = "DynamoDB table name for the URL shortener"
  type        = string
}
