output "ecr_repository_url" {
  description = "URL of the URL shortener ECR"
  value       = aws_ecr_repository.api.repository_url
}
