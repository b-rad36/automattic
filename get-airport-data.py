import pandas as pd
import requests

AIRPORT_DATA_FILENAME = 'airport-codes.csv'
AIRPORT_DATA_URL  = 'http://ourairports.com/data/airports.csv'
IATA_COLUMN_NAME = 'iata_code'

def main():
  download_airport_data(AIRPORT_DATA_URL, AIRPORT_DATA_FILENAME)
  clean_airport_data(AIRPORT_DATA_FILENAME)
  print("Finished succesfully")

def _write_to_file(filename, data):
  fo = open(filename, 'wb')
  fo.write(data)
  fo.close()

def download_airport_data(data_url, data_filename):
  print("Downloading airport data from: '" + data_url + "'...")
  airport_data = requests.get(data_url, allow_redirects=True)
  fo = open(data_filename, 'wb')
  fo.write(airport_data.content)
  fo.close()

def clean_airport_data(data_filename):
  df = pd.read_csv(data_filename)
  print("Cleaning airport data...")

  # Remove any rows with a blank IATA code
  df.dropna(subset=[IATA_COLUMN_NAME], inplace=True)

  # Rearrange the columns so IATA code is first
  new_columns = list(df.columns.values)
  new_columns.remove(IATA_COLUMN_NAME)
  new_columns.insert(0, IATA_COLUMN_NAME)
  clean_df = df.reindex(columns=new_columns)
  
  clean_df.to_csv(data_filename, encoding='utf-8', index=False)

main()
