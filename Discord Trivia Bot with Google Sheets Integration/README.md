# Discord Trivia Bot with Google Sheets Integration

This bot hosts interactive trivia games within your Discord server. Questions and answers are fetched from a Google Sheet, making it easy to update and manage your trivia content.

## Features

- **Interactive Trivia:** Engage your community with fun and challenging trivia questions.
- **Google Sheets Integration:** Easily manage questions and answers in a Google Sheet.
- **Automatic Question Loading:** Questions are loaded from the spreadsheet for each new game.
- **Reaction-Based Answers:** Participants answer by reacting to the bot's message.
- **Immediate Feedback:** The bot provides instant feedback on correct/incorrect answers.
- **Reset Functionality:** Easily reset the trivia game to start from the beginning.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Google Cloud Project:** Create a project and enable the Google Sheets API.
   - **Service Account:** Create a service account with read access to your Google Sheet and download its JSON key file (`keys.json`).
   - **Environment Variable:** Set your bot token as an environment variable named `TOKEN`.
2. **Configuration:**
   - Replace `SPREADSHEET_ID` and `RANGE_NAME` in the script with your actual Google Sheet's ID and range.
   - Place the `keys.json` file in the same directory as the script.
   - Add your trivia questions and answers (in multiple-choice format) to your Google Sheet. 
3. **Run:** Execute `python trivia_bot.py` 

## Commands

- `/trivia`: Starts the trivia game in the channel where the command is used.
- `/reset`: Resets the trivia game and clears participant data.


## How to Play

1. An authorized user starts the trivia with `/trivia`.
2. The bot posts a question from the Google Sheet with multiple-choice options.
3. Participants react to the message with the emoji corresponding to their chosen answer.
4. The bot provides immediate feedback on whether the answer is correct or incorrect.
5. After a correct answer or a set time limit, the next question is presented.
6. The game continues until all questions are answered or someone wins.
