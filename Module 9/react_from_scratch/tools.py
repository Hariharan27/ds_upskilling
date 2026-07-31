def search_transport(
    origin: str,
    destination: str,
) -> dict:
    """Search available transport options between two locations."""

    return {
        "origin": origin,
        "destination": destination,
        "options": [
            {
                "type": "train",
                "price": 6000,
            },
            {
                "type": "flight",
                "price": 24000,
            },
        ],
    }

def search_hotels(
    destination: str,
) -> dict:
    """Search available hotels at a destination."""

    return {
        "destination": destination,
        "options": [
            {
                "name": "Hotel A",
                "price": 8000,
            },
            {
                "name": "Hotel B",
                "price": 12000,
            },
        ],
    }

def calculate_trip_cost(
    transport_cost: int,
    hotel_cost: int,
) -> dict:
    """Calculate the total transport and hotel cost."""

    total_cost = transport_cost + hotel_cost

    return {
        "transport_cost": transport_cost,
        "hotel_cost": hotel_cost,
        "total_cost": total_cost,
    }
