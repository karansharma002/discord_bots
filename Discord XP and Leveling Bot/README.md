# Discord XP and Leveling Bot

This Discord bot adds an XP (experience points) and leveling system to your server. Members earn XP by participating in chat, and as they level up, they are assigned new roles that reflect their progress.

## Features

* **XP Gain:** Users earn XP randomly (3-15 points) for each message they send in regular text channels.
* **Leveling:** Users level up when their XP reaches a certain threshold. The threshold for each level is calculated as `(level + 1) * 500`.
* **Automatic Role Management:** As users level up, they are automatically assigned a corresponding "Level X" role, and their previous level role is removed.
* **Rank Visualization:** The `/rank` command generates a personalized image displaying the user's level, XP, and progress towards the next level.
* **XP Manipulation (Admin):**
    - `/addxp @user <amount>`: Adds XP to a user's account.
    - `/removexp @user <amount>`: Removes XP from a user's account.
* **Leaderboard:**
    - `/puntaje`: Displays the top 15 users with the most XP.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Permissions:** Grant the bot the "Manage Roles" permission.
   - **Environment Variable:** Set your bot token as an environment variable named `TOKEN`.
   - **Image Folder:** Place the necessary images in an `Images` folder in the same directory as the script.
2. **Data Storage:**
   - The bot uses `Data.json` to store user XP and level data. Ensure this file is present (you can start with an empty JSON object `{}`).

## Usage

1. **Run the bot:** `python xp_bot.py` 
2. **Participate in Chat:** Users will automatically earn XP as they send messages.
3. **View Rank:** Use the `/rank` command to see your current level and XP progress.
4. **Admin Commands:**
    - Use `/addxp` and `/removexp` to adjust XP manually.
    - Use `/puntaje` to display the leaderboard.


## Customization

* Modify the XP gain range in `on_message` to adjust how quickly users level up.
* Customize the image generation in the `rank` command by adjusting the image paths and text formatting.

## Important Notes

* The bot will automatically create "Level X" roles if they don't exist. Ensure the bot has the "Manage Roles" permission to do this.
* The XP and leveling system is designed for simplicity. You can expand it with additional features like rewards or level-up announcements.
