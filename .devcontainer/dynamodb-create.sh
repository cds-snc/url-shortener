aws dynamodb create-table \
   --table-name url_shortener \
   --attribute-definitions AttributeName=short_url,AttributeType=S \
   --key-schema AttributeName=short_url,KeyType=HASH \
   --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
   --endpoint-url http://dynamodb-local:8000 \
   --no-cli-pager