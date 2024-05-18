# Discord Fight Challenge Bot

This bot adds a competitive twist to your Discord server by enabling users to challenge each other to fights and track their rankings. The bot handles matchmaking, ensuring fair fights between players of similar skill levels.

## Features

- **Fight Challenges:** Members can directly challenge each other.
- **Automatic Matchmaking:** The bot pairs opponents based on their ranks.
- **Leaderboard:** Displays the top 10 ranked players.
- **Rank Calculation:**  Wins and losses affect a player's rank.
- **Visual Rank Display:** The `$rank` command showcases a player's rank with a custom image.

## Commands

**User Commands:**
- `$fight`: Enter the matchmaking queue to find an opponent.
- `$challenge @user`: Challenge a specific user to a fight.
- `$cancel`: Cancel a pending fight request.
- `$rank`: View your current rank and progress.
- `$leaderboard`: See the top 10 ranked players.

**Admin Commands:**
- `$clearqueue confirm`: (Admin only) Clears the matchmaking queue. 

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and get its token.
   - **Python:** Ensure you have Python installed.
   - **Dependencies:** Install required libraries: `pip install discord.py Pillow`
   - **Environment Variable:** Set your bot token as an environment variable named `TOKEN`.
   - **Images:** Place rank images in the "Images" folder.
2. **Data Storage:**
   - Create a `Data.json` file to store player ranks. You can start with an empty JSON object `{}`.

## How It Works

1. Users join the fight queue using `$fight` or challenge others directly with `$challenge`.
2. The bot matches players based on their ranks (stored in `Data.json`), prioritizing similar skill levels.
3. Once matched, both players are notified.
4. Players fight (presumably outside the bot), and the winner is determined.
5. An admin uses `$select_winner @user` to update the winner's rank. 

## Customization

- Adjust the `RANKS` list in the code to customize rank thresholds.
- Modify the `human_format` and image generation functions for different display styles.


