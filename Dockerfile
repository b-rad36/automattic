FROM python:3.7-slim

ENTRYPOINT ["/bin/bash"]
RUN apt-get update && apt-get install -y --no-install-recommends curl unzip && apt-get clean
RUN cd /tmp && \
	curl -s https://releases.hashicorp.com/terraform/0.13.0/terraform_0.13.0_linux_amd64.zip > \
		terraform_0.13.0.zip && \
	unzip terraform_0.13.0.zip && \
	rm    terraform_0.13.0.zip && \
	mv    terraform /usr/local/bin/

RUN curl -sL https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64 > /usr/local/bin/jq && \
	chmod 0755 /usr/local/bin/jq

COPY requirements.txt /tmp
RUN pip install --upgrade pip && pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

