# PocketBot - Enhanced Discord Economy Bot

PocketBot is a versatile Discord bot that brings an engaging economy system to your server. It allows users to earn, trade, deposit, and withdraw an in-bot currency called "Pocket Coins". 

## Features

- **Coin Rewards:** Randomly awards Pocket Coins to users who participate in chat.
- **Trading:**  Users can send Pocket Coins to each other.
- **Deposits and Withdrawals:**  Deposit Pocket Coins using Bitcoin Cash (BCH) or withdraw them to your BCH wallet or PayPal account.
- **Price Tracking:** Get the current value of Pocket Coin and Bitcoin Cash in USD.
- **Balance Checks:** View your coin balance.
- **Leaderboard:**  See the top earners on the server.
- **Self-Role Assignment:** Set up reaction-based roles for your server.
- **Slash Commands:** Modern and user-friendly interaction with the bot.
- **Security:** Robust verification system for deposits using BCH transaction hashes.

## Commands

- `/bal [@user]`: Check your or another user's balance.
- `/deposit <AMOUNT>`: Calculate the BCH deposit required for a given amount of Pocket Coins and provide instructions.
- `/send <@user> <AMOUNT>`: Send Pocket Coins to another user.
- `/withdraw <AMOUNT> <ADDRESS>`: Request a withdrawal of Pocket Coins to your BCH wallet or PayPal.
- `/verify <HASH ID>`: Verify a BCH transaction to receive your deposited Pocket Coins.
- `/leaderboard`: View the top users by Pocket Coin balance.
- `/scholars`: List all registered scholars (users).
- `/help`: Get a list of available commands.
- `/ping`: Check the bot's latency.
- `/address`: Get the BCH deposit address.

## Installation & Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Dependencies:** Install the required Python libraries: `pip install discord.py discord-py-interactions requests python-dotenv` 
   - **Configuration:** Create `Data.json` and `Transactions.json` in a "Config" folder to store user data and transaction history.
   - **Environment Variable:** Set your Discord bot token as an environment variable named `TOKEN`.

2. **Run:** `python pocketbot_enhanced.py`

## Additional Notes

* **Disclaimer:** Use this bot responsibly. The bot developers are not liable for any financial losses incurred during the use of this bot.
* **Customization:** The bot is designed to be easily customizable. You can adjust the reward amounts, transaction fees, and more.


