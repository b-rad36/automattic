#!/usr/bin/env bash

echo "Getting Systems Wrangler airport codes..."
API_URL=${1:-$(terraform output base_url)}
systems_wrangler_airports="$(curl -s 'https://ac-map.automattic.com/?g=wpcom' | jq -r '.[].host' | sort | uniq)"

output="{\"Systems Wrangler - Airports\": [ "
for airport in $systems_wrangler_airports
do
  airport_location="$(curl -s $API_URL/iata/$airport | jq -r .location)"
  output=$output$( jq -n \
    --arg air "$airport" \
    --arg loc "$airport_location" \
    '{airport: $air, location: $loc}' )
done
output="$output]}"

echo $output | sed 's/}{/},{/g' | jq > automattic-airports.json
echo "Systems Wrangler airport codes written to 'automattic-airports.json'"
