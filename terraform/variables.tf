variable "key" {
  description = "The Key"
  type        = string
  sensitive   = true
}

variable "secret" {
  description = "The secret"
  type        = string
  sensitive   = true
}

variable "telegram_token" {
  description = "The token of the bot"
  type        = string
  sensitive   = true
}
