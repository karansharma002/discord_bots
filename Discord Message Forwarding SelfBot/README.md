# Discord Message Forwarding Self Bot

This powerful Discord self-bot automates the process of forwarding messages (including embeds and attachments) from one channel to another. Ideal for mirroring content across servers, creating backups, or simply keeping tabs on multiple conversations without switching between channels.

**Key Features**

* **Seamless Forwarding:** Effortlessly replicate messages, embeds, and attachments from one Discord channel to another.
* **Customizable:** Easily configure the source-destination channel pairings in a simple JSON file.
* **Self-Bot Simplicity:** Run directly as a user bot, requiring no additional bot accounts.
* **Webhook Integration:** Leverages Discord's webhook system for efficient and reliable message delivery.

**Getting Started**

1. **Prerequisites:**
   - **Discord Account:** Use your own Discord account for the bot.
   - **Python:** Ensure Python is installed on your system.
   - **Dependencies:** Install the required libraries: `pip install discord.py aiohttp`.
   - **Bot Token:** Set your Discord user token as an environment variable named `TOKEN`.

2. **Configuration:**
   - Create a `Data.json` file in the same directory as the script.
   - Populate the file with key-value pairs where the key is the source channel ID and the value is the webhook URL of the destination channel:
   
     ```json
     {
         "SOURCE_CHANNEL_ID_1": "WEBHOOK_URL_1",
         "SOURCE_CHANNEL_ID_2": "WEBHOOK_URL_2"
     }
     ```

3. **Run the Bot:** Execute the script from your terminal: `python your_script_name.py`. The bot will log in to your Discord account and begin forwarding messages as specified in `Data.json`.

**Important Notes**

* **Self-Bot Policy:** Be aware of Discord's self-bot policy. Using self-bots excessively or for malicious purposes may result in account restrictions.
* **Webhook Creation:** You'll need to create webhooks in the destination channels beforehand. Refer to Discord's documentation for instructions.
* **Private Channels:**  This bot might not work reliably with private channels due to webhook limitations.
* **Customization:** The script can be further tailored to your specific needs, such as filtering messages based on content or adding additional features.
