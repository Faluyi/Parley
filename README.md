# Selenium Comment Bot with AI-Generated Comments

This project automates the process of posting comments on blogs using Selenium. The bot scrapes content from blogs and subreddits, uses OpenAI to generate related comment content, and posts the generated comment on a specified blog URL.

## Features

- Scrapes content from specified blogs and subreddits.
- Uses OpenAI to generate related comments based on the scraped content.
- Automatically posts the generated comments on a specified blog URL.
- Retries in case of errors during the process.

## Requirements

- Python 3.6+
- Virtual environment (optional but recommended)
- Praw
- Openai
- Selenium

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Run the setup script
Make sure to run the setup script before running the main script to install the dependencies.

## For Windows
setup.bat

Alternatively, open the project folder in the file explorer and double click the "setup.bat" script.

## macOS
chmod +x setup.sh
./setup.sh

### 3. Set up the environment variables
## For Windows
setup_env.bat

Alternatively, open the project folder in the file explorer and double click the "setup_env.bat" script.

## For macOS
chmod +x setup_env.sh
./setup_env.sh


## Usage
To run the script, execute the main script file ("main.py).
-python3 main.py


## Project Structure

README.md: This file, providing an overview of the project, setup instructions, and usage guidelines.
requirements.txt: Lists dependencies required for the project.
main.py: Contains the main script file implementing the CommentBot class and related functionalities.
scraper.py: Handles the scraping logic for blogs and subreddits.
ai_generator.py: Implements the generation of comments using OpenAI based on scraped content.
properties.py: Configuration file storing API keys and other constants.
env/: Directory containing the virtual environment setup.
setup_env.bat: Batch file to set up environment variables for Windows users.
setup_env.sh: Shell script to set up environment variables for macOS users.
setup.bat: Batch file to install needed dependencies for Windows users.
setup.sh: Shell script to install needed dependencies for macOS users.
