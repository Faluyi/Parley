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
### 2. Activate the virtual environment 
#### For windows
python -m venv venv
venv\Scripts\activate

#### For MacOS
python3 -m venv venv
source venv/bin/activate

### 3. Set Up OpenAI API Key
Make sure to set up your OpenAI API key in the properties.py file or as an environment variable. This key is necessary for generating comments.

### 4. Set Up Praw Configuration
If using Praw for scraping content from Reddit, configure Praw with your Reddit API credentials in properties.py or as environment variables.


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