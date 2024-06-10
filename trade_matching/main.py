from fastapi import FastAPI
import requests
import time

app = FastAPI()

ORDERS_SERVICE_URL = "http://order_management:8000/orders"

# A simple in-memory list to store trades for demonstration
trades = []

def fetch_orders():
    """Fetches all active orders from the Order Management Service."""
    response = requests.get(ORDERS_SERVICE_URL)
    return response.json()

def match_orders():
    """Matches buy and sell orders."""
    orders = fetch_orders()
    buys = sorted([order for order in orders.values() if order['side'] == 'buy'], key=lambda x: x['price'], reverse=True)
    sells = sorted([order for order in orders.values() if order['side'] == 'sell'], key=lambda x: x['price'])

    while buys and sells and buys[0]['price'] >= sells[0]['price']:
        # Assuming all orders are for 1 quantity
        trade = {
            'buy_order_id': buys[0]['order_id'],
            'sell_order_id': sells[0]['order_id'],
            'price': sells[0]['price'],
            'quantity': 1
        }
        trades.append(trade)
        # Notify via WebSocket (pseudo code)
        notify_trade(trade)
        buys.pop(0)
        sells.pop(0)

def notify_trade(trade):
    """Notify about the trade via WebSocket."""
    # Implementation would actually send data through WebSocket here
    print(f"Trade executed: {trade}")

@app.on_event("startup")
async def startup_event():
    while True:
        match_orders()
        time.sleep(1)  # Check for new orders every second

@app.get("/trades/")
def get_trades():
    return trades
