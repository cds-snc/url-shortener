output "url_shortener_table_name" {
  value = aws_dynamodb_table.url_shortener.id
}

output "url_shortener_table_arn" {
  value = aws_dynamodb_table.url_shortener.arn
}
