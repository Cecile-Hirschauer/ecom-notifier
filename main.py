import os
import sys

from datetime import datetime
from pathlib import Path

import json
import requests
from selectolax.parser import HTMLParser

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from a .env file
load_dotenv()

# Define the path to the price.json file
FILE_PRICE = Path(__file__).parent / 'price.json'

# Configure logging
logger.remove()
logger.add(sys.stderr, level="DEBUG")
logger.add("logs/debug.log", level="WARNING", rotation="1 MB")


def write_price_to_file(price: int):
    """
    Writes the current price to a JSON file with a timestamp.

    Args:
        price (int): The current price to write to the file.

    Returns:
        None
    """
    logger.info(f"Writing price {price} to file")

    # Check if the price file exists and load its content, otherwise initialize an empty list
    if FILE_PRICE.exists():
        with open(FILE_PRICE, 'r') as f:
            data = json.load(f)
    else:
        data = []

    # Append the current price and timestamp to the data
    data.append({
        "price": price,
        "timestamp": datetime.now().isoformat()
    })

    # Write the updated data back to the file
    with open(FILE_PRICE, 'w') as f:
        json.dump(data, f, indent=4)


def get_price_difference(current_price: int) -> int:
    """
    Calculates the difference in price as a percentage compared to the last recorded price.

    Args:
        current_price (int): The current price to compare.

    Returns:
        int: The percentage difference between the previous price and the current price.

    Raises:
        ZeroDivisionError: If the previous price is zero.
    """
    logger.info("Getting price difference")

    # Load the previous price from the file if it exists, otherwise use the current price
    if FILE_PRICE.exists():
        with open(FILE_PRICE, 'r') as f:
            data = json.load(f)
        previous_price = data[-1]['price']
    else:
        previous_price = current_price

    # Calculate the percentage difference
    try:
        return round((previous_price - current_price) / previous_price * 100)
    except ZeroDivisionError as e:
        logger.error("Previous price value is zero: division by 0 impossible")
        raise e


def send_alert(message: str):
    """
    Sends an alert message using the Pushover API.

    Args:
        message (str): The alert message to send.

    Returns:
        None

    Raises:
        requests.RequestException: If there is an error sending the alert.
    """
    logger.info(f"Sending alert: {message}")

    try:
        # Send a POST request to the Pushover API with the necessary data
        response = requests.post("https://api.pushover.net/1/messages.json",
                                 data={
                                     "token": os.environ["PUSHOVER_TOKEN"],
                                     "user": os.environ["PUSHOVER_USER"],
                                     "message": message,
                                 })
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error sending alert: {str(e)}")
        raise e


def get_current_price(asin: str) -> int:
    """
    Fetches the current price of a product from Amazon using its ASIN.

    Args:
        asin (str): The Amazon Standard Identification Number of the product.

    Returns:
        int: The current price of the product.

    Raises:
        requests.RequestException: If there is an error fetching the content.
        ValueError: If the price cannot be found in the fetched content.
    """
    proxies = {
        "http": os.environ['PROXY'],
        "https": os.environ['PROXY']
    }

    url = f"https://www.amazon.fr/dp/{asin}"

    try:
        # Fetch the page content from Amazon
        response = requests.get(url, proxies=proxies, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Couldn't fetch content from {url} due to: {str(e)}")
        raise e

    html_content = response.text

    # Parse the HTML content to find the price
    tree = HTMLParser(html_content)
    price_node = tree.css_first("span.a-price-whole")

    error_msg = f"Couldn't find price in {url}"
    if price_node:
        return int(price_node.text().replace(",", ""))

    logger.error(error_msg)
    raise ValueError(error_msg)


def main(asin: str):
    """
    Main function to check the current price of a product, calculate the difference from the previous price,
    write the current price to a file, and send an alert if the price has decreased.

    Args:
        asin (str): The Amazon Standard Identification Number of the product.

    Returns:
        None
    """
    current_price = get_current_price(asin=asin)
    price_difference = get_price_difference(current_price=current_price)
    write_price_to_file(price=current_price)

    if price_difference > 0:
        send_alert(f"Price has decreased by {price_difference}%")


if __name__ == '__main__':
    current_asin = "B0B46N7QQL"
    main(current_asin)
