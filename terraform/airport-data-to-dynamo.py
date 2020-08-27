import io
import boto3
import pandas as pd
import re
import requests
import sys

AIRPORT_DATA_FILENAME = 'airport-codes.csv'
AIRPORT_DATA_URL      = 'http://ourairports.com/data/airports.csv'
AUTOMATTIC_DATA_URL   = 'https://ac-map.automattic.com/?w=570h=285'
BATCH_SIZE            = 100
COLOR_CODE            = 'color_code'
COLOR_NAME            = 'color'
IATA_CODE             = 'iata_code'
COLUMN_NAMES          = [IATA_CODE, 'municipality', 'iso_country', COLOR_NAME, COLOR_CODE]
LOCATION_REGEX        = 'dcss\[\"[a-z]{3}\"].*'

# Takes a command-line argument for the name of the DynamoDB Table where
# the data is being uploaded to. Creates a table representing information about Automattic datacenters
# as they appear on the map for the Systems Wrangler job posting.
def main():
  TABLE_NAME = sys.argv[1]

  print("Downloading airport data from: '" + AIRPORT_DATA_URL + "'...")
  airport_df = pd.read_csv(AIRPORT_DATA_URL)

  print("Getting info about Automattic data centre locations...")
  automattic_df = get_automattic_locations_df(AUTOMATTIC_DATA_URL)

  print("Combining airport and location data...")
  cleaned_airport_df = combine_airport_location_data(airport_df, automattic_df)

  print("Writing data to DynamoDB...")
  write_to_dynamodb_from_df(cleaned_airport_df, get_dynamo_table(TABLE_NAME))

  print("Finished succesfully")


# Gathers data about the map representations of the datacenter locations. Puts that data into
# a data frame
def get_automattic_locations_df(automattic_url):
  location_df    = pd.DataFrame(columns=[IATA_CODE, COLOR_NAME, COLOR_CODE])
  location_data  = requests.get(automattic_url).content
  location_lines = re.findall(LOCATION_REGEX, location_data.decode("utf-8"))
  for line in location_lines:
    location_df = location_df.append({
      IATA_CODE:  line.split('"')[1].upper(),
      COLOR_NAME: line.split('\t')[-1].split(' ')[-1],
      COLOR_CODE: re.search("#\w{6}", line).group()
    }, ignore_index=True)
  return location_df


# Combines data from the airport dataframe and the Automattic datacenter location dataframe
def combine_airport_location_data(airport_df, location_df):
  new_airport_df = airport_df.reindex(columns=COLUMN_NAMES)
  df = pd.merge(new_airport_df, location_df, on=IATA_CODE, how='right')
  df.drop_duplicates(subset=[IATA_CODE], inplace=True)
  df.drop(columns=[COLOR_NAME + "_x", COLOR_CODE + "_x"], inplace=True)
  df.rename(columns={COLOR_NAME + "_y": COLOR_NAME, COLOR_CODE + "_y": COLOR_CODE}, inplace=True)
  df.sort_values(by=[IATA_CODE], inplace=True)
  return df

# Returns the table object representing a DynamoDB table
def get_dynamo_table(table_name):
  dynamodb = boto3.resource('dynamodb')
  try:
     table = dynamodb.Table(table_name)
  except:
     print("Error loading DynamoDB table.")
     exit(1)
  return table

# Takes a dataframe and writes the data to a DynamoDB table
def write_to_dynamodb_from_df(dataframe, dynamo_table):
  batch = []
  for row in dataframe.to_dict('records'):
    if len(batch) >= BATCH_SIZE:
       _write_batch_to_dynamo(batch, dynamo_table)
       batch.clear()
 
    batch.append(row)
 
  if batch:
     _write_batch_to_dynamo(batch, dynamo_table)

# Write a batch of rows to a DynamoDB table
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
