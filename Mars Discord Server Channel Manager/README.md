# Mars Discord Server Channel Manager

This Discord bot helps automate routine channel management tasks and provides a simple verification system for new members.

## Features

* **Channel Updates:**
    - Automatically updates date and time channels in UTC timezone.
    - Displays the current total online members and total members in designated channels.
* **Member Verification:**
    - Presents a welcome message to new members with a "VERIFY" button.
    - When the button is clicked, it assigns the "Member" role and removes the "Unverified" role.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Permissions:** Grant the bot the following permissions:
     - `Manage Channels` (to edit channel names)
     - `Manage Roles` (for verification)
   - **Channels:** Create channels for the date, time, online count, and member count.
   - **Roles:** Create "Unverified" and "Member" roles.
   - **Environment Variable:** Set your bot token as an environment variable named `TOKEN`.
2. **Configuration:**
    - Replace the placeholder `guild_id` and channel IDs in the script with your actual values.
    - Set the `unverified_role_name` and `member_role_name` to match your server's roles.

## Usage

- **Run the bot:** `python channel_manager_bot.py`
- **Setup Verification:** Use the slash command `/setupverify` in the desired channel.
- The bot will automatically handle channel updates and verification.

## Customization

- You can modify the update interval and the format of the date/time in the `update_channels` task.
- The welcome message and verification process can be easily customized in the code. 


## Important Notes:

- Make sure your bot has the correct permissions in the relevant channels.
- For security, keep your bot token confidential.
