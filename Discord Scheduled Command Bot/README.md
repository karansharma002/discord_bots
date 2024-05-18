# Discord Scheduled Command Bot

This Discord bot allows you to schedule up to two custom commands to be automatically executed at specific times each day in a designated channel. It's a simple yet powerful tool for automating recurring tasks within your Discord server.

## Features

* **Scheduled Commands:** Schedule up to two commands to run daily at specified times (UTC timezone).
* **Channel Targeting:** Choose the channel where the scheduled commands will be executed.
* **Customization:** Easily set the commands and times using simple bot commands.
* **Persistent Storage:** The scheduled tasks and settings are saved in a JSON file (`Settings.json`), ensuring they persist even if the bot restarts.


## How to Use

1. **Prerequisites:**
   - **Discord Bot:** Create a Discord bot and obtain its token.
   - **Environment Variable:** Set your bot token as an environment variable named `BOT_TOKEN`.
2. **Installation:**
   - Clone this repository.
   - Run `pip install -r requirements.txt` (you'll need `discord.py` and `python-dateutil`).
3. **Configuration:**
   - Run the bot once. It will create a `Settings.json` file in the same directory.
   - Edit `Settings.json` to set your desired commands, times, and channel ID:
     ```json
     {
         "Channel": YOUR_CHANNEL_ID,
         "COMMAND": "YOUR_COMMAND_HERE",
         "TIME1": "DD/MM/YY HH:MM:SS",  // Example: 25/12/23 12:00:00
         "TIME2": "DD/MM/YY HH:MM:SS"   // Example: 25/12/23 18:30:00
     }
     ```
   - Replace `YOUR_CHANNEL_ID` and `YOUR_COMMAND_HERE` with your actual values.
   - Use 24-hour format for time (HH:MM:SS) and ensure the date format is DD/MM/YY.
4. **Run the bot:** `python your_script_name.py`

## Commands

* **%setchannel <#channel>:** Sets the channel where the scheduled commands will be executed.
* **%settime <TIME1> <TIME2>:** Sets the two times for the scheduled commands (use 24-hour format, e.g., "14:30").
* **%setcommand <command>:** Sets the command to be executed.


## Examples

```
%setchannel #general     
%settime 08:00 16:00
%setcommand !daily_update 
```

## Important Notes

* The bot will automatically execute the scheduled commands at the specified times each day.
* The scheduled times are based on UTC timezone.
* If a scheduled time is in the past (within the same day), the command will be executed immediately and rescheduled for the next day.
