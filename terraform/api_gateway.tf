resource "aws_api_gateway_rest_api" "airport_iata_codes" {
  name        = "AirportIataCodes"
  description = "API to get the municipality and country of airports"
}

resource "aws_api_gateway_resource" "iata_root" {
   rest_api_id = aws_api_gateway_rest_api.airport_iata_codes.id
   parent_id   = aws_api_gateway_rest_api.airport_iata_codes.root_resource_id
   path_part   = "iata"
}

resource "aws_api_gateway_resource" "MyDemoResource" {
  rest_api_id = aws_api_gateway_rest_api.airport_iata_codes.id
  parent_id   = aws_api_gateway_resource.iata_root.id
  path_part   = "{iata+}"
}

resource "aws_api_gateway_method" "proxy" {
   rest_api_id   = aws_api_gateway_rest_api.airport_iata_codes.id
   resource_id   = aws_api_gateway_resource.MyDemoResource.id
   http_method   = "GET"
   authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
   rest_api_id = aws_api_gateway_rest_api.airport_iata_codes.id
   resource_id = aws_api_gateway_method.proxy.resource_id
   http_method = aws_api_gateway_method.proxy.http_method

   integration_http_method = "POST"
   type                    = "AWS_PROXY"
   uri                     = aws_lambda_function.airport_iata_codes.invoke_arn
}

resource "aws_api_gateway_deployment" "deployment" {
   depends_on = [aws_api_gateway_integration.lambda]

   rest_api_id = aws_api_gateway_rest_api.airport_iata_codes.id
   stage_name  = "bradley_gavan"
}

output "base_url" {
  value = aws_api_gateway_deployment.deployment.invoke_url
}

