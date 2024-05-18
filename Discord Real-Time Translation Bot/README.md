# Discord Real-Time Translation Bot

This Discord bot seamlessly translates messages between English and Spanish channels in real time. It leverages Google Translate for accurate translations and webhooks to maintain the original author's identity in translated messages.

## Features

* **Real-Time Translation:** Instantly translates messages between designated English and Spanish channels.
* **Preserves Author Identity:** Translated messages are sent via webhook, displaying the original author's name and avatar.
* **Easy Channel Management:** Simple commands to add or remove translation channel pairs.
* **Toggle Translation:** Enable or disable translation as needed.


## How to Use

1. **Prerequisites:**
   - **Discord Bot:** Create a Discord bot and obtain its token.
   - **Google Cloud Project:** Create a Google Cloud Project and enable the Translation API. (Free tier available for limited usage)
   - **Environment Variable:** Set your bot token as an environment variable named `BOT_TOKEN`.
2. **Installation:**
   - Clone this repository.
   - Run `pip install -r requirements.txt` to install the necessary libraries.
3. **Configuration:**
   - Create three JSON files in the same directory as the script:
     - `EN.json`: Store English channel IDs as keys and their corresponding Spanish channel IDs as values.
     - `SP.json`: Store Spanish channel IDs as keys and their corresponding English channel IDs as values.
     - `Languages.json`: Define the language codes for translation (e.g., `{"english": "en", "spanish": "es"}`). You can add more languages if needed. 
4. **Run the bot:** `python your_script_name.py`
5. **Bot Commands:**
   - `!translate enable`:  Activates the translation functionality.
   - `!translate disable`: Deactivates the translation functionality.
   - `!translate add #channel1 #channel2`: Adds a translation pair where `#channel1` is the English channel and `#channel2` is the Spanish channel (or vice versa).


## Examples

```
!translate enable          # Start translating
!translate add #english #spanish  # Link channels for translation
```


## Important Notes

* The bot will automatically translate any message sent in a linked channel pair.
* To avoid translation of commands, start commands with the '&' prefix (e.g., `&translate enable`).
* Make sure your bot has the "Manage Webhooks" permission in the channels you want to translate.
