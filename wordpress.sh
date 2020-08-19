x="$(curl -s 'https://ac-map.automattic.com/?g=wpcom' | jq -r '.[].host' | sort | uniq)"
a="$(curl -s 'http://www.airportcodes.org/' | grep '<br />')"
for i in $x
do
  echo "$a" | grep -i "($i)" | awk '//{print $1 $2 }' | sort
done
