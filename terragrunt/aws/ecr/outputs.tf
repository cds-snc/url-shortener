output "ecr_repository_url" {
  description = "URL of the URL shortener ECR"
  value       = aws_ecr_repository.api.repository_url
}

output "ecr_repository_arn" {
  description = "Arn of the ECR Repository"
  value       = aws_ecr_repository.api.arn
}
