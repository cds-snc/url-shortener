# Generated by Terragrunt. Sig: nIlQXj57tbuaRZEa
terraform {
  backend "s3" {
    bucket         = "url-shortener-staging-tf"
    dynamodb_table = "terraform-state-lock-dynamo"
    encrypt        = true
    key            = "./terraform.tfstate"
    region         = "ca-central-1"
  }
}
