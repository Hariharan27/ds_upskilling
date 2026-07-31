from tools import (
search_transport,
search_hotels,
calculate_trip_cost,
)

TOOL_REGISTRY = {
    "search_transport": search_transport,
    "search_hotels": search_hotels,
    "calculate_trip_cost": calculate_trip_cost,
}


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "search_transport",
            "description": (
            "Search for available transport options and their prices "
            "between an origin and destination. "
            "Use this tool when actual transport options or costs are needed."
        ),
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "The origin of the transport",
                    },
                    "destination": {
                        "type": "string",
                        "description": "The destination of the transport",
                    }
                },
                "required": ["origin", "destination"],
            }
        }
    },{
        "type": "function",
        "function": {
            "name": "search_hotels",
            "description": (
            "Search for available hotel options and their prices "
            "at the destination. "
            "Use this tool when actual accommodation options or costs are needed."
        ),
            "parameters": {
                "type": "object",
                "properties": {
                    "destination": {
                        "type": "string",
                        "description": "The travel destination.",
                    }
                }
            },
            "required": ["destination"],
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_trip_cost",
             "description": (
            "Calculate the total trip cost using selected transport "
            "and hotel costs. "
            "Call this tool only after the actual transport and hotel "
            "costs are available from previous tool observations. "
            "Never guess or invent the input costs."
        ),
            "parameters": {
                "type": "object",
                "properties": {
                      "transport_cost": {
                        "type": "integer",
                        "description": "The selected transport cost.",
                    },
                    "hotel_cost": {
                        "type": "integer",
                        "description": "The selected hotel cost.",
                    },
                },
                "required": ["transport_cost", "hotel_cost"],
            }
        }
    }
]

def get_tool(name:str):
    """Return the registered tool for the given name."""
    return TOOL_REGISTRY.get(name)

