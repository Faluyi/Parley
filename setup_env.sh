#!/bin/bash

# Check if the .bash_profile file exists
if [ ! -f ~/.bash_profile ]; then
    touch ~/.bash_profile
fi

# Add environment variables to .bash_profile
echo "export PARLEY_API_KEY='your_openai_api_key'" >> ~/.bash_profile
echo "export PARLEY_CLIENT_ID='your_client_id'" >> ~/.bash_profile
echo "export PARLEY_CLIENT_SECRET='your_client_secret'" >> ~/.bash_profile

# Source the .bash_profile to apply changes
source ~/.bash_profile

echo "Environment variables have been set and applied."
