# Counting and Guessing Game Discord Bot

This Discord bot offers two fun games for your server:

1. **Counting Game:** Members take turns counting in a channel, with the bot enforcing the rules.
2. **Number Guessing Game:** The bot chooses a secret number, and members try to guess it.


## Counting Game Features

- **Automated Moderation:**  The bot deletes invalid messages and ensures players count in order.
- **Configurable Limit:**  Set a target number for the counting game.
- **Win Announcement:**  The bot announces when the target number is reached.
- **Simple Setup:** Use slash commands to start and manage the game.

## Number Guessing Game Features

- **Random Number Generation:** The bot chooses a secret number within a specified range.
- **Hints:** The bot tells players if their guesses are too high or too low.
- **Win Announcement:** The bot congratulates the winner and ends the game.
- **Error Handling:** The bot handles invalid input and provides feedback to players.

## Setup & Commands

1. **Prerequisites:**
   - Create a Discord bot and obtain its token.
   - Set your bot token as an environment variable named `TOKEN`.
   - Install required libraries: `pip install discord.py python-dotenv`

2. **Bot Commands:**

   - **Counting Game:**
     - `/count <channel> <target_number>`: Starts the counting game in the specified channel.
     - `/reset`: Resets the counting game.

   - **Number Guessing Game:**
     - `/guess <channel> <min_number> <max_number>`: Starts the guessing game in the specified channel.



## How to Play

**Counting Game:**

1. Use the `/count` command to start the game, specifying a channel and the target number to reach.
2. Members take turns sending messages with consecutive numbers.
3. The bot deletes any incorrect messages or attempts to skip numbers.
4. The game ends when someone reaches the target number.

**Number Guessing Game:**

1. Use the `/guess` command to start the game, specifying a channel and the range of numbers to guess from.
2. Members take turns guessing the secret number.
3. The bot provides hints (higher/lower) with each guess.
4. The game ends when someone guesses the correct number.

## Additional Notes

- **Permissions:** The bot requires the "Manage Messages" permission to delete incorrect messages.
- **Error Handling:** The bot provides feedback for invalid input and other errors.
- **Customization:** You can easily modify the bot's messages, embeds, and other aspects to suit your server's style.
