import os
import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "https://live.trading212.com/api/v0"
auth = HTTPBasicAuth(os.environ["T212_API_KEY"], os.environ["T212_API_SECRET"])

TICKER = "AAPL_US_EQ"
TARGET_QTY = 1.0  # Maximum shares to hold

# 1. Fetch current portfolio positions
res = requests.get(f"{BASE_URL}/equity/portfolio", auth=auth)
res.raise_for_status()
portfolio = res.json()

# 2. Check current holdings for the target ticker
current_qty = 0.0
for item in portfolio:
    if item.get("ticker") == TICKER:
        current_qty = float(item.get("quantity", 0.0))
        break

print(f"Current {TICKER} holdings: {current_qty} shares")

# 3. Execute rule: Buy only if below target quantity
if current_qty < TARGET_QTY:
    qty_to_buy = round(TARGET_QTY - current_qty, 4)
    print(f"Placing market buy order for {qty_to_buy} shares of {TICKER}...")
    order = requests.post(
        f"{BASE_URL}/equity/orders/market",
        json={"ticker": TICKER, "quantity": qty_to_buy},
        auth=auth
    )
    print("Order response:", order.status_code, order.json())
else:
    print("Target already met. No order placed.")
