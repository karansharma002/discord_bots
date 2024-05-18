# Discord Voice Channel Recording Bot

This Discord bot automatically joins designated voice channels and records the audio for 45 minutes. It is designed to help server administrators capture and archive voice conversations for moderation, content creation, or other purposes.

## Features

* **Automatic Recording:**  The bot joins a specified voice channel and starts recording at a set interval.
* **Periodic Recording:**  By default, recordings are made every 45 minutes.
* **Multi-User Recording:** Records audio from multiple users within the same voice channel.
* **Individual Audio Files:** Saves each user's audio in separate MP3 files, labeled with their Discord user ID.
* **Data Storage:** Recording details (filename, duration) are saved in a JSON file (`Data.json`).

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Permissions:** Grant the bot the "Connect" and "Speak" permissions in the voice channel you want to record.
   - **Bot Token:** Replace 'TOKEN_ID' in the script with your actual bot token.
   - **Libraries:**  Install the required libraries:
     ```bash
     pip install discord.py
     ```
2. **Configuration:**
   - Set the `guild_id` and `channel_id` variables in the script to the IDs of your server and the desired voice channel, respectively.
   - Optionally, you can adjust the recording interval in the `extract_data` task (default is 45 minutes).

## How It Works

1. The bot starts the `extract_data` task in a loop.
2. At the specified interval (or when someone joins the channel), the bot joins the voice channel.
3. It starts recording audio from all users in the channel.
4. After 45 minutes, the recording ends, and each user's audio is saved as a separate MP3 file.
5. The file names and durations are logged in `Data.json`.

## Additional Considerations

* **Privacy:** Inform users that their voice conversations may be recorded.
* **Storage:** Manage the storage of audio files as they can accumulate over time.
* **Discord Limits:** Be mindful of Discord's limitations on voice connections and file sizes.
* **Error Handling:** The bot includes basic error handling. Consider expanding this for more robust operation.

