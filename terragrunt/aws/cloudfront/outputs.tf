output "cloudfront_api_arn" {
  description = "ARN of the API's CloudFront distribution."
  value       = aws_cloudfront_distribution.url_shortener_api.arn
}