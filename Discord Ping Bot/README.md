# Discord Ping Bot

This bot monitors specific channels for keywords or phrases and then notifies designated roles when those keywords are found. It's designed to streamline communication and ensure important messages get noticed.

## Features

* **Keyword/Phrase Triggers:** Create rules to ping specific roles when certain words or phrases appear in channel messages or embeds.
* **Multiple Rules:** Set up multiple rules for different channels and roles.
* **Customizable Notifications:** Tailor the notification message to include the mentioned role and relevant information.
* **Hash-Based Management:** Use unique hashes to easily manage and delete rules.
* **Backup and Restore:** Safeguard your rule configurations with backup and restore commands.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Permissions:** Grant the bot the "Send Messages," "Read Message History," and "Manage Roles" permissions in the relevant channels.
   - **Environment Variable:** Set your bot token as an environment variable named `TOKEN`.

2. **Configuration:**
   - Create a `Rules.json` file in a folder named `Ping_Bot` in the same directory as the script to store rules (start with an empty file: `{}`).
   - Use the `pb!add` command to create rules (see below for usage).

## Commands

* **pb!add #channel @role +keyword1[/keyword2/...] $message:** 
   - Adds a new rule to ping `@role` when `keyword1`, `keyword2`, etc., are found in `#channel`.
   - Replace `$` in the message with the role mention to ping them directly.
   - Separate multiple keywords with `/` within the keyword section.
* **pb!delete hash:** Deletes a rule using its unique hash ID.
* **pb!channels:** Lists channels where rules are currently active.
* **pb!fetchrule #channel:** Displays all rules and their hashes for the specified channel.
* **pb!backup:** Creates a backup of your rule configurations in `Backup.json`.
* **pb!restore:** Restores rule configurations from `Backup.json`.
* **pb!addkeyword hash +keyword:** Adds a keyword to an existing rule.
* **pb!removekeyword hash +keyword:** Removes a keyword from an existing rule.

## Usage Examples
pb!add #general @Announcements +giveaway $Attention @Announcements! A new giveaway has started!
pb!fetchrule #general  # View all rules for the #general channel
pb!delete 12345ABCDE    # Delete a rule using its hash

## Important Notes
* **Keyword Format:** Keywords are case-insensitive and should be prefixed with `+`. You can use multiple keywords separated by `/`.
* **Message Format:** The notification message should start with `$`, which will be replaced with the mentioned role.
* **Permissions:** Ensure the bot has the necessary permissions to manage roles and send messages in the configured channels.
