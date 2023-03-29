aws dynamodb delete-table --table-name url_shortener --endpoint-url http://dynamodb-local:8000 --no-cli-pager

aws dynamodb create-table \
   --table-name url_shortener \
   --attribute-definitions AttributeName=key_id,AttributeType=S AttributeName=email,AttributeType=S \
   --key-schema AttributeName=key_id,KeyType=HASH \
   --global-secondary-indexes IndexName=emailIndex,KeySchema=["{AttributeName=email,KeyType=HASH}"],Projection="{ProjectionType=ALL}",ProvisionedThroughput="{ReadCapacityUnits=1,WriteCapacityUnits=1}" \
   --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
   --endpoint-url http://dynamodb-local:8000 \
   --no-cli-pager \
