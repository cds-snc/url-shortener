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

        # Load secrets
        aws ssm get-parameters \
          --region ca-central-1 \
          --with-decryption \
          --names \
              auth_token_app \
              auth_token_notify \
              cloudfront_header \
              hashing_peppers \
              login_token_salt \
              notify_api_key \
              notify_contact_email \
          --query 'Parameters[*].Value' \
          --output text | sed 's/\t\t*/\n/g' > "$TMP_ENV_FILE"
    fi

    # Check if secrets were retrieved
    if [ ! -s "$TMP_ENV_FILE" ]; then
        echo "Failed to retrieve secrets"
        rm "$TMP_ENV_FILE"
        exit 1
    fi
    load_non_existing_envs
    
    echo "Starting lambda handler"
    exec /usr/local/bin/python -m awslambdaric "$1"
fi
