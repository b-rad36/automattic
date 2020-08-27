#!/usr/bin/env bash

echo "Getting Systems Wrangler airport codes..."
API_URL=${1:-$(terraform output base_url)}
systems_wrangler_airports="$(curl -s 'https://ac-map.automattic.com/?g=wpcom' | jq -r '.[].host' | sort | uniq)"

output="{\"Systems Wrangler - Airports\": [ "
for airport in $systems_wrangler_airports
do
  airport_data="$(curl -s $API_URL/iata/$airport)"
  airport_location="$(echo $airport_data | jq -r .location)"
  color="$(echo $airport_data | jq -r .color)"
  output=$output$( jq -n \
    --arg air "$airport" \
    --arg loc "$airport_location" \
    --arg col "$color" \
    '{airport: $air, location: $loc, color: $col}' )
done
output="$output]}"

echo $output | sed 's/}{/},{/g' | jq > automattic-airports.json
echo "Systems Wrangler airport codes written to 'automattic-airports.json'"
