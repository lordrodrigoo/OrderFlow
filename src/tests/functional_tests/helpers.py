from datetime import datetime, timedelta


def create_order(client, address_id, amount, headers, delivery_fee=5.00):
    response = client.post("/api/v1/orders/", json={
        "address_id": address_id,
        "total_amount": amount,
        "delivery_fee": delivery_fee,
        "scheduled_date": (datetime.now() + timedelta(days=1)).isoformat()
    }, headers=headers)
    assert response.status_code == 201
    return response.json()
