#!/bin/bash

# Set the filename where the key will be saved
KEY_FILE="./sheets-key.json"

# Fetch the private key JSON from Terraform output and save to file
terraform output -raw sheets_key_json > "$KEY_FILE"

# Check if file was created successfully
if [[ -f "$KEY_FILE" ]]; then
  echo "Saved service account key to $KEY_FILE"
else
  echo "Failed to save the service account key"
  exit 1
fi

# Export the environment variable for this session
export GOOGLE_APPLICATION_CREDENTIALS="$KEY_FILE"
echo "Exported GOOGLE_APPLICATION_CREDENTIALS=$KEY_FILE"

# Optionally, add export to your shell profile for persistence
echo "Add the following line to your ~/.bashrc or ~/.zshrc to persist the env variable:"
echo "export GOOGLE_APPLICATION_CREDENTIALS=\"$KEY_FILE\""
