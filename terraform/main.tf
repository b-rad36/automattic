variable "aws_profile" {
  description = "AWS Profile to use for the deployment"
  type        = string
}

variable "aws_region" {
  description = "AWS Region the resources will be deploymed to"
  type        = string
}
variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table that will be created and populated"
  type        = string
}

provider "aws" {
  profile = var.aws_profile
  region  = var.aws_region
  version = "~> 2.0"
}

#https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_table
resource "aws_dynamodb_table" "airport_dynamodb_table" {
  name         = var.dynamodb_table_name 
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "iata_code"

  attribute {
    name = "iata_code"
    type = "S"
  }
 
  provisioner "local-exec" {
    command     = "python3 airport-data-to-dynamo.py ${var.dynamodb_table_name}"
    environment = {
      AWS_PROFILE         = var.aws_profile
      AWS_DEFAULT_REGION  = var.aws_region
    }
  }
}
