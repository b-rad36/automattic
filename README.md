# Data Centres
There are 32 data centres, 28 of which appear on the map. The 28 are as follow:
  * Amsterdam, NL (Orange)
  * Atlanta, US (Iron)
  * Burbank, US (Lime)
  * Chicago, US (Caramel)
  * Dallas-Fort Worth, US (White)
  * Denver, US (Turquoise)
  * Frankfurt am Main, DE (Sky)
  * Hong Kong, HK (Pink)
  * Johannesburg, ZA (Jade)
  * London, GB (Red)
  * Madrid, ES (Uranium)
  * Miami, US (Yellow)
  * Milan, IT (Forest)
  * Mumbai, IN (Lime)
  * Newark, US (Navy)
  * Osaka, JP (Violet)
  * Paris, FR (Wine)
  * San Jose, US (Damson)
  * São Paulo, BRi (Zinnia)
  * Seattle, US (Khaki)
  * Singapore, SG (Pink)
  * Stockholm, SE (Honeydew)
  * Sydney, AU (Quagmire)
  * Taipei, TW (Crimson)
  * Tokyo / Narita, JP (Green)
  * Toronto, CA (Coral)
  * Vienna, AT (Xanthin)
  * Washington, US (Amethyst)
  
The other 4 data centres are:
  * Kunduz, Afghanistan (Ebony)
  * Kunduz, Afghanistan (Mallow)
  * Los Angeles, US (Blue)
  * San Antonio, US (Orpiment)
  
## How I found this informatiion
All this information I found by Examining the network traffic from the job posting page (https://automattic.com/work-with-us/systems-wrangler/). I found an inital call to get the map which provided all of the datacentre locations and their colors. After that, there are recurring calls to update the map which gave me the information of which data centers actually appear on the map.

THe locations in the network calls are represented by 3 letter codes. I recognized these as airport codes (know as IATA codes). At this point, I could have just used the IATA codes to do a quick search and learned the location of each data centres. I instead looked for an API that would be able to give me that info and I I could simply put all this into a script. Unfortunately, I didn't find and free APIs for airport data so I decided to make my own.

## What's in this repo?
This repo contains a combination of Terraform code, Bash and Python scripts and a Dockerfile.

What this project does is use Terraform to create various pieces of AWS infrastrure. Specifically it creates an API Gateway, Lambda and DynamoDB Table. 
1. There is a  hook in the Terraform code that runs the 'airport-data-to-dynamo.py' script. This script populates the DynamoDB Table with all the data about Automattic's data centres
2. The Lambda takes an IATA (airport) code and returns a JSON object containing the code, location and color of the data center.
3. The Lambda is run by means of the API Gateway.
4. There is a second Terraform hook that will run the `get-airport-info.sh` script. This script will use the API Gateway endpoint to get all of the data centre info from the API and output it to `terraform/automattic-airports.json`.

# Running the code
## Prerequesites
  * Have docker and docker-compose (version 1.25.0+) installed
  * Have an AWS Profile configured in your local `~/.aws/credentials`. Ideally, this Profile will have an admin permission and be for a development environment.

## Env Vars
Make sure to fill in the variables in the `.env` file.

## Build the docker image
Note that you will need to use tag 'brad' as that is what referenced in `docker-compose.yml`  
```$ docker build -t brad .```

## Start the container
```$ docker-compose run --rm automattic```

## From the container
#### Verify that your AWS Profile is configured properly. If not check, `.env` and `~/.aws/credentials`.  
```$ aws sts get-caller-identity > /dev/null 2>&1 || { echo 'AWS vars not configured'; exit 1; }```

#### Initialize Terraform
```$ terraform init```

#### Create the infrastructure
```$ terraform apply```

#### When finished, destroy the infrastrure
```$ terraform destroy```

#### Or, all in one command:
```$ terraform init && terraform apply --auto-approve && terraform destroy --auto-approve```

## Check the output of `get-airport-info.sh` script
Note that the script is run automatically every time `$ terraform apply` is run.  
`$ cat terraform/automattic-airports.json`



