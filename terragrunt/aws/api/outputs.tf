output "function_arn" {
  description = "ARN of the lambda function"
  value       = module.url_shortener_lambda.function_arn
}

output "function_name" {
  description = "Name of the lambda function"
  value       = module.url_shortener_lambda.function_name
}

output "invoke_arn" {
  description = "The ARN used to invoke the Lambda function"
  value       = module.url_shortener_lambda.invoke_arn
}
