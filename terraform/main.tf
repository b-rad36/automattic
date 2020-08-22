variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table that will be created and populated"
  default     = "airport-data"
  type        = string
}

provider "aws" {
  version = "~> 2.0"
}

provider "null" {
  version = "~> 2.0"
}

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
  }
}

resource "null_resource" "get_airports" {
  depends_on = [
	aws_dynamodb_table.airport_dynamodb_table, 
	aws_lambda_function.airport_iata_codes,
        aws_iam_role_policy_attachment.lambda_dynamodb_attach,
	aws_api_gateway_deployment.deployment ]
  
  triggers = {
    always_run = "${timestamp()}"
  }

  provisioner "local-exec" {
    command = "bash -c 'sleep 15; ./get-airport-info.sh ${aws_api_gateway_deployment.deployment.invoke_url}'"
    }
}

