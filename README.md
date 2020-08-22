# automattic

# Prerequesites
## Install Docker
## Install docker-compose (version 1.25.0+)
## Have an AWS user, ideally with admin permissions for an environemnt
## Have the AWS user credentials configured in ~/.aws/credentials

# Fill in docker-compose.yml ENV vars

$ docker build -t brad .
$ docker-compose run --rm automattic

$ terraform init && terraform apply --auto-approve && terraform destroy --auto-approve

$ cat automattic-airports.json

