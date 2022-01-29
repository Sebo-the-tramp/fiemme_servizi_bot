resource "aws_dynamodb_table" "basic-dynamodb-table" {
  name           = "fiemme_servizi_users"
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "chat_id"

  attribute {
    name = "chat_id"
    type = "N"
  }

  tags = {
    Name        = "dynamodb-table-1"
    Environment = "production"
  }
}
