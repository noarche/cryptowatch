import requests
import time
from datetime import datetime
from colorama import init, Fore, Style

# ---------------- USER-DEFINED OPTIONS ---------------- #
SLEEP_TIME = 2         # Time between updates in seconds (e.g., 2 seconds = 2000ms)
COINS_DISPLAYED = 10   # Number of top coins to display in the console
# ------------------------------------------------------- #

# Initialize colorama
init(autoreset=True)

# Function to fetch data from the API
def fetch_data():
    response = requests.get('https://api.coincap.io/v2/assets')
    if response.status_code == 200:
        return response.json()['data']
    else:
        print(Fore.RED + "Error fetching data from API")
        return None

# Helper function to format large numbers like volume
def format_volume(volume):
    if volume >= 1_000_000_000:
        return f"{volume / 1_000_000_000:.2f}B"
    elif volume >= 1_000_000:
        return f"{volume / 1_000_000:.2f}M"
    elif volume >= 1_000:
        return f"{volume / 1_000:.2f}K"
    else:
        return f"{volume:.2f}"

# Function to display the data in a well-designed format
def display_data(data, previous_data):
    print(Style.BRIGHT + Fore.CYAN + f"{'RANK':<6}{'NAME':<15}{'PRICE (USD)':<15}{'24H VOL':<15}{'24H CHANGE':<10}")
    print("-" * 60)
    
    for item in data[:COINS_DISPLAYED]:  # Display the number of coins defined by COINS_DISPLAYED
        symbol = item['symbol']
        name = item['name']
        rank = item['rank']
        price = float(item['priceUsd'])
        volume_24hr = format_volume(float(item['volumeUsd24Hr']) if item['volumeUsd24Hr'] else 0)
        percent_change_24h = float(item['changePercent24Hr']) if item['changePercent24Hr'] else 0.0

        # Determine color for price change
        price_color = Fore.WHITE
        if symbol in previous_data:
            prev_price = float(previous_data[symbol]['priceUsd'])
            if price > prev_price:
                price_color = Fore.GREEN
            elif price < prev_price:
                price_color = Fore.RED
        
        # Formatting percentage change color
        change_color = Fore.GREEN if percent_change_24h > 0 else Fore.RED

        # Display the data with coloring
        print(f"{rank:<6}{name:<15}{price_color}${price:<14.2f}{volume_24hr:<15}{change_color}{percent_change_24h:.2f}%")

# Main loop
def main():
    previous_data = {}
    
    while True:
        data = fetch_data()
        if data:
            # Sort the data by rank and ensure BTC is always on top
            sorted_data = sorted(data, key=lambda x: int(x['rank']) if x['symbol'] != 'BTC' else 0)
            
            # Clear the console
            print("\033[H\033[J", end="")
            
            # Display the data
            display_data(sorted_data, previous_data)
            
            # Save the current prices for the next update comparison
            previous_data = {item['symbol']: item for item in sorted_data}
        
        # Wait for the user-defined time before the next update
        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    main()

