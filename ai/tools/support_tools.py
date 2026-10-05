from langchain_core.tools import tool

ORDERS: dict[str, dict[str, object]] = {
    "DS-1001": {
        "order_id": "DS-1001",
        "customer_id": "cust_demo",
        "status": "delivered",
        "item_summary": "Wireless headphones",
        "total": "79.99",
        "currency": "USD",
        "delivery_status": "delivered",
        "delivered_at": "2026-10-04 14:32 UTC",
        "carrier": "ParcelPost",
        "tracking_id": "PP-DEMO-1001",
    },
    "DS-1002": {
        "order_id": "DS-1002",
        "customer_id": "cust_demo",
        "status": "in_transit",
        "item_summary": "Desk lamp",
        "total": "42.00",
        "currency": "USD",
        "delivery_status": "in_transit",
        "delivered_at": "",
        "carrier": "ParcelPost",
        "tracking_id": "PP-DEMO-1002",
    },
    "DS-9001": {
        "order_id": "DS-9001",
        "customer_id": "cust_other",
        "status": "delivered",
        "item_summary": "Private customer order",
        "total": "15.00",
        "currency": "USD",
        "delivery_status": "delivered",
        "delivered_at": "2026-10-04 10:00 UTC",
        "carrier": "ParcelPost",
        "tracking_id": "PP-PRIVATE-9001",
    },
}


@tool
def get_order(order_id: str, customer_id: str) -> dict[str, object] | None:
    """Retrieve an order only when it belongs to the authenticated customer."""
    order = ORDERS.get(order_id.upper())
    if order is None or order["customer_id"] != customer_id:
        return None
    return {key: value for key, value in order.items() if key != "customer_id"}


@tool
def get_delivery_status(order_id: str, customer_id: str) -> dict[str, str] | None:
    """Retrieve tracking status for an order owned by the authenticated customer."""
    order = ORDERS.get(order_id.upper())
    if order is None or order["customer_id"] != customer_id:
        return None
    return {
        "status": str(order["delivery_status"]),
        "delivered_at": str(order["delivered_at"]),
        "carrier": str(order["carrier"]),
        "tracking_id": str(order["tracking_id"]),
    }