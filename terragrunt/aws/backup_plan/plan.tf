#
# Backup plans for default 
#

# Default backup plan
resource "aws_backup_plan" "backup_plan_default" {
  name = "backup_plan_default"
  rule {
    rule_name         = "backup_rule_default"
    target_vault_name = aws_backup_vault.vault.name
    schedule          = local.plan_schedule_default
    start_window      = 60

    lifecycle {
      cold_storage_after = local.cold_storage_after_default
      delete_after       = local.delete_after_default
    }
  }

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}
