@echo off
echo Setting up environment variables for Parley...

:: Prompt the user for API key
set /p parley_api_key="Enter your Parley API key: "
:: Prompt the user for Client ID
set /p parley_client_id="Enter your Parley Client ID: "
:: Prompt the user for Client Secret
set /p parley_client_secret="Enter your Parley Client Secret: "

:: Set environment variables
setx parley_api_key "%parley_api_key%"
setx parley_client_id "%parley_client_id%"
setx parley_client_secret "%parley_client_secret%"

echo Environment variables have been set.
pause
