# Discord Invite Tracker and Stats Bot

This Discord self-bot tracks member invitations, provides a leaderboard of top inviters, and displays real-time statistics related to a specific blockchain address.

## Features

* **Invite Tracking:**  Automatically monitors and records which users are invited by whom.
* **Leaderboard:** Displays a leaderboard of the top 20 inviters in the server.
* **Statistics:**  Fetches and displays BNB balance and the latest ERC-720 burn transaction details from BscScan.
* **Reset Leaderboard:** Allows an admin to reset the invite leaderboard data.
* **Self-Bot:** Runs as a user bot, requiring no additional bot accounts.


## Setup

1. **Prerequisites:**
   - **Discord Account:** Use your own Discord account for the bot.
   - **Python:** Ensure Python is installed on your system.
   - **Dependencies:** Install the required libraries: `pip install discord.py aiohttp selenium`.
   - **Chromedriver:** Download and install the latest Chromedriver executable from the official website.
   - **Bot Token:** Set your Discord user token as an environment variable named `TOKEN`.
   - **BscScan API Key:** Get an API key from BscScan and update the `url` variable in the script.
2. **Configuration:**
   - Create a `Data.json` file in the same directory as the script to store invite data (you can start with an empty file: `{}`).
   - Update `url2` with the BscScan URL for your desired address.
   - Set the `gld` variable to the ID of your Discord server.

3. **Run the bot:** `python your_script_name.py`

## Commands

* **!invites @user:** Displays the total number of invites a user has.
* **!leaderboard:** Shows the top 20 inviters in the server.
* **!reset confirm:** Resets the leaderboard data (requires typing "confirm" for safety).
* **!stats:** Fetches and displays BNB balance and ERC-720 burn details.

## How It Works

* **Invite Tracking:** When a member joins, the bot records who invited them. This data is stored in `Data.json`.
* **Leaderboard:** The bot calculates and displays the top inviters based on the data in `Data.json`.
* **Statistics:**  The bot uses Selenium to scrape the BscScan page and the BscScan API to fetch BNB balance.

## Important Notes

* **Self-Bot Policy:** Be aware of Discord's self-bot policy. Using self-bots excessively or for malicious purposes may result in account restrictions.
* **ChromeDriver:**  Make sure the Chromedriver executable is in your system's PATH or specify the path directly in the script.
* **Error Handling:** The bot includes basic error handling for invite fetching and data scraping.
* **Privacy:** The bot only fetches and displays public information from BscScan.

## Disclaimer

This bot is provided as-is and should be used responsibly. Cryptocurrency trading and interactions involve financial risks. The author is not responsible for any losses incurred while using this script.
