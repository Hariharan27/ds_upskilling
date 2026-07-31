from langchain_core.tools import StructuredTool

from app.models import (
    CalculateTripCostInput,
    CalculateTripCostResult,
    HotelOption,
    SearchHotelsInput,
    SearchHotelsResult,
    SearchTransportInput,
    SearchTransportResult,
    TransportOption,
)


def search_transport(
    origin: str,
    destination: str,
) -> SearchTransportResult:
    """
    Search available transport options between two locations.

    This currently returns mock data for learning purposes.
    """

    return SearchTransportResult(
        origin=origin,
        destination=destination,
        options=[
            TransportOption(
                type="train",
                total_price=6000,
            ),
            TransportOption(
                type="flight",
                total_price=24000,
            ),
        ],
    )


search_transport_tool = StructuredTool.from_function(
    func=search_transport,
    name="search_transport",
    description=(
        "Search for available transport options and prices "
        "between an origin and destination. "
        "Use this tool when transport information is required."
    ),
    args_schema=SearchTransportInput,
)


def search_hotels(
    destination: str,
) -> SearchHotelsResult:
    """
    Search available hotel options at a destination.

    This currently returns mock data for learning purposes.
    """

    return SearchHotelsResult(
        destination=destination,
        options=[
            HotelOption(
                name="Hotel A",
                total_price=8000,
            ),
            HotelOption(
                name="Hotel B",
                total_price=12000,
            ),
        ],
    )

search_hotels_tool = StructuredTool.from_function(
    func=search_hotels,
    name="search_hotels",
    description=(
        "Search for available hotel options and prices "
        "at a destination. "
        "Use this tool when accommodation information is required."
    ),
    args_schema=SearchHotelsInput,
)


def calculate_trip_cost(
    transport_total_price: int,
    hotel_total_price: int,
) -> CalculateTripCostResult:
    """
    Calculate the total cost of selected transport and hotel options.
    """

    print(
        "\n>>> CALCULATE_TRIP_COST EXECUTED:",
        transport_total_price,
        hotel_total_price,
    )

    return CalculateTripCostResult(
        transport_total_price=transport_total_price,
        hotel_total_price=hotel_total_price,
        total_trip_price=transport_total_price + hotel_total_price,
    )


calculate_trip_cost_tool = StructuredTool.from_function(
    func=calculate_trip_cost,
    name="calculate_trip_cost",
    description=(
        "Calculate the total trip cost using selected transport "
        "and hotel costs. Use actual costs obtained from available "
        "information or previous tool observations. "
        "Do not invent or guess cost values."
    ),
    args_schema=CalculateTripCostInput,
)

TOOLS = [
    search_transport_tool,
    search_hotels_tool,
    calculate_trip_cost_tool,
]
