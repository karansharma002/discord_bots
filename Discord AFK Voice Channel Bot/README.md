# Discord AFK Voice Channel Bot

This simple yet handy Discord bot automatically moves members to a designated AFK (Away From Keyboard) voice channel when they self-deafen. It helps keep your active voice channels clutter-free and provides a dedicated space for AFK members.

## Features

* **Automatic AFK Movement:**
    - Detects when a user self-deafens in any voice channel.
    - Automatically moves the user to the specified AFK voice channel.
* **Easy Setup:** 
    - Use the `!setchannel` command to designate an AFK channel.
* **Error Handling:**
    - Includes basic error handling to log any issues that may occur.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Permissions:** Grant the bot the "Move Members" permission.
   - **Environment Variable:** Set your bot token as an environment variable named `TOKEN`.
2. **Installation & Run:**
   - Install `discord.py`: `pip install discord.py`
   - Run the bot: `python your_script_name.py`

## Usage

1. **Set AFK Channel:**
   - In a text channel, use the command `!setchannel #channel_name` to designate the AFK voice channel (e.g., `!setchannel #afk`).

2. **Self-Deafen:**
   - When a member self-deafens in any voice channel, the bot will automatically move them to the designated AFK channel.
   - **Note:** The bot currently only reacts to self-deafening; it does not move members who are server-deafened.

## Customization (Optional)

* **Additional Triggers:** You could modify the bot to move members based on other criteria (e.g., inactivity for a certain time, muting).
* **Notification:** You could add a feature to notify users when they're moved to the AFK channel.

## Limitations

* **Permissions:** Ensure the bot has the "Move Members" permission in all voice channels, including the designated AFK channel.
* **Error Handling:** While the bot includes basic error logging, you might want to add more robust error handling for specific scenarios (e.g., channel not found, insufficient permissions).
