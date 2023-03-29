locals {

  region = "ca-central-1"

  # Default Backup plan
  plan_schedule_default        = "cron(0 12 * * ? *)" # every day at 12:00
  plan_schedule_default_testing= "cron(0 12 * * ? *)" # once every 10 minutes for testing
  cold_storage_after_default   = 30
  delete_after_default         = 120
}
