output "url_shortener_table_name" {
  description = "The name of the url shortener table name"
  value       = aws_dynamodb_table.url_shortener.id
}

output "url_shortener_table_arn" {
  description = "The arn of the url shortener table name"
  value       = aws_dynamodb_table.url_shortener.arn
}
