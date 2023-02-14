variable "function_name" {
  description = "The lambda function name"
  type        = string
}

variable "function_url" {
  description = "The lambda function url"
  type        = string
}

variable "hosted_zone_id" {
  description = "The hosted zone ID to create DNS records in"
  type        = string
}

variable "enable_waf" {
  description = "(Optional) Should the WAF be enabled? Defaults to true."
  type        = bool
  default     = true
}

variable "vpc_id" {
  description = "The VPC id of the url shortener"
  type        = string
}