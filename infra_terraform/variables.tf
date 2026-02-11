variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "sonic-agent"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "availability_zones" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b"]
}

variable "cognito_domain_prefix" {
  type        = string
  description = "Must be globally unique"
}

variable "knowledge_base_id" {
  type = string
}

variable "dynamodb_table_name" {
  type = string
}

variable "container_cpu" {
  type    = number
  default = 1024
}

variable "container_memory" {
  type    = number
  default = 2048
}

variable "desired_count" {
  type    = number
  default = 2
}
