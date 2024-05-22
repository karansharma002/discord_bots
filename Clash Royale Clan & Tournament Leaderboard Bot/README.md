## Clash Royale Clan & Tournament Leaderboard Bot

This Discord bot seamlessly integrates with the Clash Royale API to provide real-time updates on clan member rankings and tournament leaderboards.

**Features**

*   **Clan Leaderboard:** Fetches and displays the top 10 clan members based on trophies.
*   **Tournament Leaderboard:** Tracks and shows the top 3 players in a specified tournament.
*   **Automated Updates:** Refreshes leaderboards every 23 hours.
*   **Customization:**  Admins can configure the clan tag, tournament ID, and output channels.
*   **Testing Command:** Admins can test the API connection and data fetching.

## Setup

1.  **Prerequisites:**
    *   **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
    *   **Clash Royale API Key:** Obtain an API key from the Clash Royale developer portal.
    *   **Permissions:** Grant the bot the "Send Messages" and "Embed Links" permissions in the designated channels.
    *   **Environment Variables:** Set your Discord bot token as `DISCORD_BOT_TOKEN` and your Clash Royale API token as `CLASH_ROYALE_API_TOKEN`.

2.  **Configuration:**
    *   The bot will automatically create a `Settings.json` file upon first run.
    *   Use the following commands to configure the bot (replace placeholders with actual values):
        *   `!setclan #YOURCLANTAG` (without the #)
        *   `!setchannel #CHANNEL_NAME` (the channel where you want the leaderboards to be posted)
        *   `!settournament #YOURTOURNAMENTID` (without the #)

3.  **Run the bot:** `python your_script_name.py`

## Commands

*   **`!setclan <clantag>` (Admin only):** Sets the clan tag to track.
*   **`!setchannel <#channel>` (Admin only):** Sets the channel for leaderboard updates.
*   **`!settournament <tournament_id>` (Admin only):** Sets the tournament ID to track.
*   **`!test` (Admin only):** Tests the bot's functionality by fetching and displaying data.
*   **`!clear [amount]` (Admin only):** Clears a specified number of messages in the current channel (defaults to 1).


## Notes

*   This bot uses the Clash Royale API and is subject to its rate limits. Ensure you don't exceed the API's usage limits.
*   **Sensitive Information:** Avoid sharing your bot token and API keys publicly. Consider using environment variables or a secure configuration file for better security.
*   **Error Handling:** Basic error handling is implemented. You can add more comprehensive error handling for potential issues with the API.

