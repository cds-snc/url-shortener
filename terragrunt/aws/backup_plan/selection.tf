#
# Backup selection
#

# Selection for default workloads
resource "aws_backup_selection" "selection_default" {
  iam_role_arn = aws_iam_role.role_backup.arn
  name         = "backup_selection_default"
  plan_id      = aws_backup_plan.backup_plan_default.id
  resources    = ["${var.url_shortener_table_arn}"]

  selection_tag {
    type  = "STRINGEQUALS"
    key   = "backup_plan"
    value = "default"
  }
}
