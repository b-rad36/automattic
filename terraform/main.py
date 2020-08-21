import boto3
import json

#ENV var
IATA_CODE    = 'iata_code'
ISO_COUNTRY  = 'iso_country'
ITEM         = 'Item'
MUNICIPALITY = 'municipality'
TABLE_NAME   = 'airport-data'

def lambda_handler(event, context):
  client = boto3.client('dynamodb')
  iata_path_code = event['path'].split('/')[-1].upper()
  response = client.get_item(
    TableName = TABLE_NAME,
    Key       = { IATA_CODE:{ 'S': iata_path_code }},
    ProjectionExpression = 'municipality, iso_country'
  )

  data = {}
  data['location'] = response[ITEM][MUNICIPALITY]['S'] + ", " + response[ITEM][ISO_COUNTRY]['S']

  return {
    'statusCode': 200,
    'body': json.dumps(data)
  }
