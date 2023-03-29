resource "aws_dynamodb_table" "url_shortener" {

  name         = "url_shortener"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "key_id"

  server_side_encryption {
    enabled = true
  }

  attribute {
    name = "key_id"
    type = "S"
  }

  attribute {
    name = "email"
    type = "S"
  }

  global_secondary_index {
    name            = "emailIndex"
    hash_key        = "email"
    projection_type = "ALL"
  }

  point_in_time_recovery {
    enabled = true
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}
