#!/usr/bin/env bash
cd terraform
echo "Getting 'Systems Wrangler' airport codes..."
systems_wrangler_airports="$(curl -s 'https://ac-map.automattic.com/?g=wpcom' | jq -r '.[].host' | sort | uniq)"

output="{\"Systems Wrangler - Airports\": [ "
for airport in $systems_wrangler_airports
do
  output=$output$( jq -n \
    --arg air "$airport" \
    --arg loc "$(curl -s $(terraform output base_url)/iata/$airport | jq -r .location)" \
    '{airport: $air, location: $loc}' )
done
output="$output]}"

echo $output | sed 's/}{/},{/g' | jq

