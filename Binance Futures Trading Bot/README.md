# Binance Futures Trading Bot

This Python script is designed to automate trading on Binance Futures. It provides functionality for placing single or multiple orders with stop-loss and take-profit levels, as well as canceling orders and setting a maximum loss threshold.

## Features

* **Single Order Placement:** Execute individual long/short orders with customizable TP and SL percentages.
* **Multiple Order Placement:** Manage multiple orders across different symbols with their own TP and SL settings.
* **Stop-Loss and Take-Profit:** Automatically set stop-loss and take-profit orders to control risk and lock in profits.
* **Max Loss Control:** Define a total loss amount that, when reached, will cancel all active orders.
* **Order Cancellation:** Easily cancel all pending orders for a specific symbol.
* **API Key Management:** Securely stores your Binance API keys in a separate JSON file.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://your_repo_url.git 
   ```
2. **Install dependencies:**
   ```bash
   pip install python-binance 
   ```
3. **Create `credentials.json`:**
   - Place a file named `credentials.json` in the same directory as the script.
   - Fill it with your Binance API key and secret key:
   ```json
   {
       "api_key": "YOUR_API_KEY",
       "secret_key": "YOUR_SECRET_KEY"
   }
   ```
4. **Create `Data.json`:**
    - Place a file named `Data.json` in the same directory as the script
    - Fill it with the sum amount that should be lost at max:
    ```json
    {
        "Sum Amount": -50
    }
    ```

## Usage

Run the script from your terminal:

```bash
python your_script_name.py
```

Follow the on-screen menu to choose your desired actions.

## Configuration

* **Take Profit and Stop Loss:**  Customize the TP and SL percentages for each order based on your trading strategy.
* **Max Loss:** Adjust the maximum allowed loss amount to your risk tolerance.

## Disclaimer

This bot is provided as-is and should be used with caution. Cryptocurrency trading involves significant risk, and the author is not responsible for any financial losses incurred while using this script.

## Contributing

Feel free to submit pull requests or open issues if you find bugs or have feature suggestions.


**Key points:**

* **Clear Structure:** The README is well-organized with sections for features, installation, usage, configuration, and a disclaimer.
* **Concise Instructions:** The installation and usage steps are easy to follow.
* **Important Information:**  The disclaimer highlights the risks involved in trading.
* **No Unnecessary Elements:** The README avoids logos and pictures, making it simple to copy and use.