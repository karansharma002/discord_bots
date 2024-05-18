# Shopee Phone Verification Bot

This Discord bot simplifies phone number verification for Shopee accounts by integrating with the sms-activate service. Users can purchase virtual phone numbers and receive verification codes directly within a Discord ticket system.

## Features

* **Ticket-Based Interaction:** Users initiate a purchase by creating a ticket with the `=purchase` command.
* **Balance Checking:** Users can check their point balance using `=check_balance`.
* **Country Selection:** Offers virtual phone numbers from Indonesia and Vietnam.
* **OTP Retrieval:** Automatically fetches the OTP (One-Time Password) from sms-activate and displays it to the user.
* **Error Handling:** Includes basic error handling for insufficient balance and invalid responses.

## Setup

1. **Prerequisites:**
   - **Discord Bot:** Create a bot on the Discord Developer Portal and obtain its token.
   - **sms-activate Account:** Create an account on sms-activate.org and obtain an API key.
   - **Permissions:** Grant the bot the "Manage Channels" permission.
   - **Environment Variable:** Set your bot token as an environment variable named `TOKEN`.
   - **API Key:**  Replace `KEY` in the script with your sms-activate API key.
2. **Data Storage:**
   - Create a `Data.json` file to store user balances (you can start with an empty file: `{}`).


## Usage

1. Run the bot: `python shopee_bot.py`
2. **Purchase:**
   - Users type `=purchase` to initiate a ticket.
   - The bot guides the user through country selection and number purchase.
   - The bot provides the phone number and automatically fetches the OTP.

3. **Check Balance:**
   - Users type `=check_balance` to see their available points.

4. **Add Points (Admin Only):**
   - Administrators can add points to a user's balance using `=add <amount>`.

## Important Notes

* **Point System:** The bot assumes you have a point system in place (e.g., users can buy points through other means).
* **sms-activate Costs:** Using sms-activate requires purchasing credits on their platform.
* **Customization:** You can modify the countries offered, the cost per number, and error messages to suit your needs.
* **Security:** Keep your bot token and sms-activate API key confidential.
* **Rate Limits:** Be aware of the rate limits imposed by both Discord and sms-activate. 
