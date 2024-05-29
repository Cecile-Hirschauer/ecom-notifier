# Ecom-Notifier

## Overview
Ecom-Notifier is an ethical web scraping project designed to monitor price changes for a specific product on Amazon. When a price decrease is detected, the tool sends a notification to the user via the Pushover service.

## Features
- Monitor the price of a product on Amazon using its ASIN (Amazon Standard Identification Number).
- Log the current price along with a timestamp.
- Calculate the percentage difference between the current and previous prices.
- Send notifications of price decreases using Pushover.
- Uses Brightdata Web Unlocker proxy for handling web scraping.

## Requirements
- Python 3.12
- Brightdata Web Unlocker proxy
- Pushover account for notifications

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ecom-notifier.git
    cd ecom-notifier
    ```

2. Create and activate a virtual environment:
    ```sh
    python3.12 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root directory of the project and add your Brightdata and Pushover credentials:
    ```env
    PUSHOVER_TOKEN=your_pushover_token
    PUSHOVER_USER=your_pushover_user
    PROXY=your_brightdata_proxy
    ```

## Usage

1. Set the ASIN of the product you want to monitor in the `main` function within `ecom_notifier.py`:
    ```python
    if __name__ == '__main__':
        current_asin = "B0B46N7QQL"
        main(current_asin)
    ```

2. Run the script:
    ```sh
    python ecom_notifier.py
    ```

## Functions

### `write_price_to_file(price: int)`
Writes the current price to a JSON file with a timestamp.

### `get_price_difference(current_price: int) -> int`
Calculates the percentage difference between the previous and current prices.

### `send_alert(message: str)`
Sends an alert message using the Pushover API.

### `get_current_price(asin: str) -> int`
Fetches the current price of a product from Amazon using its ASIN.

### `main(asin: str)`
Main function to check the current price of a product, calculate the difference from the previous price, write the current price to a file, and send an alert if the price has decreased.

## Logging
The script uses the `loguru` library for logging. Logs are written to the console and to a rotating log file located at `logs/debug.log`.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer
This project is intended for educational and ethical purposes only. Ensure you comply with Amazon's terms of service and scraping policies.

