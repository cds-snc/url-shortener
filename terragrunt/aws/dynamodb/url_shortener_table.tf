resource "aws_dynamodb_table" "url_shortener" {

  name         = "url_shortener"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "short_url"

  server_side_encryption {
    enabled = true
  }

  attribute {
    name = "short_url"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  global_secondary_index {
    name            = "ShortUrlIndex"
    hash_key        = "short_url"
    projection_type = "ALL"
  }
}