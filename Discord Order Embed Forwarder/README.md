# Discord Order Embed Forwarder

This Discord bot automatically forwards purchase confirmation embeds from one channel to another, masking sensitive information like email addresses and passwords. It is particularly useful for managing order confirmations in Discord communities.

## Features

* **Automatic Forwarding:** Listens for order confirmation embeds in a designated channel.
* **Privacy Protection:**  Removes or masks sensitive customer data (emails, passwords, etc.) before forwarding.
* **Customization:** Easily configure the source and target channels, as well as which fields to remove or replace.
* **MongoDB Integration:**  Connects to a MongoDB database to retrieve replacement information (e.g., replacing usernames).

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a Discord bot and obtain its token.
   - **MongoDB:** Set up a MongoDB database and collection.
   - **Environment Variable:** Set your bot token as an environment variable named `BOT_TOKEN`.
2. **Configuration (`config.json`):**
    ```json
    {
        "host": "YOUR_MONGODB_HOST",
        "port": YOUR_MONGODB_PORT,
        "database": "YOUR_DATABASE_NAME",
        "collection": "YOUR_COLLECTION_NAME"
    }
    ```
3. **MongoDB Data:** Ensure your MongoDB collection contains documents with the following structure:
    ```json
    {
        "User": "REPLACEMENT_USERNAME",
        "Profiles": "['[email address removed]', '[email address removed]']" // Comma-separated list of emails
    }
    ```
4. **Run the Bot:** `python your_script_name.py`

## Configuration

* **Channel IDs:** Update the source and target channel IDs in the script to match your server setup.
* **Field Filters:** Modify the `fields_to_remove` and `fields_to_replace` lists in the script to customize which fields are handled.


## How it Works

1. The bot monitors a designated channel for messages containing embeds.
2. If an embed description mentions a "successful checkout," it processes the embed.
3. Sensitive fields are removed or replaced with information from the MongoDB database if applicable.
4. The modified embed is forwarded to the target channel.

## Important Notes

* The bot requires the `python-binance`, `pymongo`, and `discord.py` libraries. Install them using pip: `pip install python-binance pymongo discord.py`
* The configuration file `config.json` must be present in the same directory as the script.
* Ensure your MongoDB database is correctly configured and populated with user data.
* For security, keep your bot token and MongoDB credentials private.
