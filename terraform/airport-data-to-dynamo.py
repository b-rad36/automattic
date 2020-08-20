import io
import boto3
import pandas as pd
import requests
import sys

AIRPORT_DATA_FILENAME = 'airport-codes.csv'
AIRPORT_DATA_URL      = 'http://ourairports.com/data/airports.csv'
BATCH_SIZE            = 100
IATA_CODE             = 'iata_code'
COLUMN_NAMES          = [IATA_CODE, 'municipality', 'iso_country']

def main():
  TABLE_NAME = sys.argv[1]

  print("Downloading airport data from: '" + AIRPORT_DATA_URL + "'...")
  airport_df = pd.read_csv(AIRPORT_DATA_URL)

  print("Cleaning airport data...")
  cleaned_airport_df = clean_airport_data(airport_df)

  print("Writing data to DynamoDB...")
  write_to_dynamodb_from_df(cleaned_airport_df, get_dynamo_table(TABLE_NAME))

  print("Finished succesfully")

# Trim unwanted columns, remove null/empty data, sort data
def clean_airport_data(dataframe):
  df = dataframe.reindex(columns=COLUMN_NAMES)
  df.dropna(inplace=True)
  df.drop(df[df.iata_code == '0'].index, inplace=True)
  df.drop(df[df.iata_code == '-'].index, inplace=True)
  df.drop_duplicates(subset=[IATA_CODE], inplace=True)
  df.sort_values(by=[IATA_CODE], inplace=True)
  return df

def get_dynamo_table(table_name):
  dynamodb = boto3.resource('dynamodb')
  try:
     table = dynamodb.Table(table_name)
  except:
     print("Error loading DynamoDB table.")
     exit(1)
  return table

def write_to_dynamodb_from_df(dataframe, dynamo_table):
  batch = []
  for row in dataframe.to_dict('records'):
    if len(batch) >= BATCH_SIZE:
       _write_batch_to_dynamo(batch, dynamo_table)
       batch.clear()
 
    batch.append(row)
 
  if batch:
     _write_batch_to_dynamo(batch, dynamo_table)

def _write_batch_to_dynamo(rows, dynamo_table):
  try:
    with dynamo_table.batch_writer() as batch:
      for i in range(len(rows)):
        batch.put_item(
           Item=rows[i]
        )
  except Exception as e:
    print("Error executing batch_writer")
    print(str(e))


main()
