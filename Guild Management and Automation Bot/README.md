# Guild Management and Automation Bot

This Discord bot enhances your server's member management and automates specific tasks related to new member onboarding, boost notifications, and message forwarding to a WordPress site.

## Features

* **Welcome Messages:** Greets new members with a personalized image and message.
* **Verification Process:** Guides new members through a verification process in DMs.
* **Boost Notifications:** Sends a thank you message when the server receives a boost.
* **Modmail:** Forwards DMs from users to a designated staff channel.
* **Staff Replies:** Allows staff to easily reply to modmail messages.
* **WordPress Integration (Optional):**  Automatically posts messages from specific channels to a WordPress blog (requires additional configuration).

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **Image:** Place the welcome image (`Welcome.png`) and the font file (`kink.TTF`) in a "Config" folder in the bot's directory.
   - **Permissions:** Grant the bot relevant permissions:
      - "Send Messages"
      - "Embed Links"
      - "Manage Members"
      - "Read Message History"
   - **Environment Variable:** Set your bot token as an environment variable named `TOKEN`.
   - **(Optional) WordPress:** If you want to use the WordPress integration, you'll need a WordPress website with the REST API enabled and Basic Authentication configured.
2. **Configuration:**
   - Replace placeholders (e.g., channel IDs) in the script with your actual values.
   - (Optional) Follow the `!setup` command instructions to configure WordPress integration.

## Usage

* **Verification:** New members will be automatically DM'd with verification instructions.
* **Commands:**
   - `)imnew`: Provides information to new members after verification.
   - `)verify`: Allows users to start the verification process if they missed it initially.
   - `)reply @user <text>`: (Staff only) Reply to a user's modmail message.
   - `)setup`: (Staff only) Set up the WordPress integration. 
   - `)addchannel #channel`: (Staff only) Add a channel to monitor for WordPress posts.

**Important Notes:**

* **Privacy:**  Be transparent with your server members about the recording of voice channels.
* **Data Storage:**  Manage the storage of voice recordings as they can accumulate over time.
* **Limitations:**  Be aware of Discord's limitations on file sizes and voice connections.

