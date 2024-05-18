# UnoRe DeFi Notification Bot for Discord

This Discord bot is specifically designed to monitor DeFi (Decentralized Finance) events on the UnoRe platform and forward them to other channels in a more readable format. It currently focuses on tracking changes in Selene's capacity and includes placeholders for future enhancements (loan updates and low balance alerts).

## Features

* **Selene Capacity Monitoring:**  Fetches real-time updates from the Selene contract on Binance Smart Chain (BSC) and posts them in a designated Discord channel.
* **Enhanced Readability:** Translates raw blockchain data into user-friendly messages that display the amount of capacity change in USD.
* **Extensibility:** The bot is structured to easily incorporate additional DeFi event notifications in the future (e.g., loans, low balances).

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Python:** Ensure you have Python 3.7 or higher installed.
   - **Dependencies:** Install the required libraries: `pip install discord.py aiohttp web3`.
   - **Environment Variable:** Set your Discord bot token as an environment variable named `TOKEN`.
   - **Webhook URLs:** Obtain the webhook URLs for the destination channels you want to forward notifications to.

2. **Configuration:**
   - In your Python script (`unore_bot.py`), update the following:
     - `TOKEN`: Your Discord bot's token.
     - `CHANNEL_IDS`: A dictionary mapping the source channel IDs to the webhook URLs of their corresponding destination channels (see example in the code).

3. **Run the bot:** `python unore_bot.py` 

## How it Works

1. The bot monitors specific Discord channels on the UnoRe server for messages related to Selene capacity changes.
2. When a relevant message is detected, it extracts the necessary information (amount, pool, staker).
3. It uses the CoinGecko API to fetch the current price of UNO (Selene's token) to calculate the USD value of the capacity change.
4. The bot formats the information into a clear message and sends it to the designated channel using a Discord webhook.

## Future Enhancements (Planned)

- **Loan Updates:** Notify when new loans are created or existing loans are modified.
- **Low Balance Alerts:**  Warn users when their account balances fall below a certain threshold.
- **Customizable Thresholds:** Allow users to set their own notification preferences.

## Disclaimer

This bot is provided as-is for informational purposes. It interacts with blockchain data and financial information. Use it at your own risk. The author is not responsible for any financial decisions or outcomes based on this bot's information.
