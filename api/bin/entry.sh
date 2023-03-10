#!/bin/sh
# shellcheck disable=SC2120

set -e

ENV_PATH="/tmp/url-shortener"
TMP_ENV_FILE="$ENV_PATH/.env"

# Check if a variable exists in the execution environment and is not empty
var_expand() {
  if [ -z "${1-}" ] || [ $# -ne 1 ]; then
    printf 'var_expand: expected one argument\n' >&2;
    return 1;
  fi
  eval printf '%s' "\"\${$1?}\"" 2> /dev/null # Variable double substitution to be able to check for variable
}

# Export variables from a .env file into the current execution environment
load_non_existing_envs() {
  _isComment='^[[:space:]]*#'
  _isBlank='^[[:space:]]*$'
  while IFS= read -r line; do
    if echo "$line" | grep -Eq "$_isComment"; then # Ignore comment line
      continue
    fi
    if echo "$line" | grep -Eq "$_isBlank"; then # Ignore blank line
      continue
    fi
    key=$(echo "$line" | cut -d '=' -f 1)
    value=$(echo "$line" | cut -d '=' -f 2-)

    if [ -z "$(var_expand "$key")" ]; then # Check if environment variable doesn't exist
      export "${key}=${value}"
    fi
  done < $TMP_ENV_FILE
}

# Local testing
if [ -z "${AWS_LAMBDA_RUNTIME_API}" ]; then
    echo "Running aws-lambda-rie"
    exec /usr/bin/aws-lambda-rie /usr/local/bin/python -m awslambdaric "$1"

# Running in AWS Lambda
else
    echo "Retrieving environment parameters"
    if [ ! -f "$ENV_PATH/.env" ]; then
        if [ ! -d "$ENV_PATH" ]; then
            mkdir "$ENV_PATH"
        fi

        aws ssm get-parameters \
            --region ca-central-1 \
            --with-decryption \
            --names api_auth_token \
            --query 'Parameters[*].Value' \
            --output text > "$TMP_ENV_FILE"
        
        aws ssm get-parameters \
            --region ca-central-1 \
            --with-decryption \
            --names hashing_peppers \
            --query 'Parameters[*].Value' \
            --output text >> "$TMP_ENV_FILE"
    fi
    load_non_existing_envs

   echo "Starting lambda handler"
   exec /usr/local/bin/python -m awslambdaric "$1"
fi
