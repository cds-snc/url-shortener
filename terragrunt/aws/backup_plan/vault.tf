resource "aws_backup_vault" "vault" {
  name = "vault"
}



resource "aws_backup_vault_policy" "vault_policy" {
  backup_vault_name = aws_backup_vault.vault.name

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "default",
  "Statement": [
    {
      "Sid": "default",
      "Effect": "Allow",
      "Principal": {
        "AWS": "${aws_iam_role.role_backup.arn}"
      },
      "Action": [
        "backup:CopyIntoBackupVault",
        "backup:DescribeBackupVault"
      ],
      "Resource": "${aws_backup_vault.vault.arn}"
    }
  ]
}
POLICY
}
