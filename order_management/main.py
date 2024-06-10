from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4

app = FastAPI()

class Order(BaseModel):
    order_id: str = None
    quantity: int
    price: float
    side: str  # "buy" or "sell"

orders = {}

@app.post("/orders/")
def create_order(order: Order):
    order_id = str(uuid4())
    order.order_id = order_id
    orders[order_id] = order
    return order

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id in orders:
        return orders[order_id]
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}")
def update_order(order_id: str, updated_order: Order):
    if order_id in orders:
        orders[order_id] = updated_order
        updated_order.order_id = order_id
        return updated_order
    raise HTTPException(status_code=404, detail="Order not found")

@app.delete("/orders/{order_id}")
def delete_order(order_id: str):
    if order_id in orders:
        del orders[order_id]
        return {"message": "Order deleted"}
    raise HTTPException(status_code=404, detail="Order not found")
