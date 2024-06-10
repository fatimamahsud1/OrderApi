from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from uuid import uuid4, UUID

app = FastAPI()

class Order(BaseModel):
    quantity: int
    price: float
    side: int  # 1 for buy, -1 for sell

class OrderUpdate(BaseModel):
    price: Optional[float] = None
    quantity: Optional[int] = None

orders: Dict[UUID, Order] = {}

@app.post("/orders/", response_model=UUID)
def create_order(order: Order):
    order_id = uuid4()
    orders[order_id] = order
    return order_id

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: UUID):
    if order_id in orders:
        return orders[order_id]
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}", response_model=bool)
def update_order(order_id: UUID, order_update: OrderUpdate):
    if order_id in orders:
        current_order = orders[order_id]
        if order_update.price is not None:
            current_order.price = order_update.price
        if order_update.quantity is not None:
            current_order.quantity = order_update.quantity
        orders[order_id] = current_order
        return True
    return False

@app.delete("/orders/{order_id}", response_model=bool)
def delete_order(order_id: UUID):
    if order_id in orders:
        del orders[order_id]
        return True
    return False

@app.get("/orders/", response_model=Dict[UUID, Order])
def list_orders():
    return orders
