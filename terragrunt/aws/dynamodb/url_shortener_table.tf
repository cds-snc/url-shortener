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

  ttl {
    attribute_name = "ttl"
    enabled        = true 
  }

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}
