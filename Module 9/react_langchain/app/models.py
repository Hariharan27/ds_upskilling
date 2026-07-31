from pydantic import BaseModel,Field

class SearchTransportInput(BaseModel):
    origin: str = Field(
        ...,
        description="The city or location where the journey starts.",
        min_length=1,
    )

    destination: str = Field(
        ...,
        description="The city or location where the journey ends.",
        min_length=1,
    )

class TransportOption(BaseModel):
    type: str

    total_price: int = Field(
        ...,
        ge=0,
        description=(
            "The total round-trip transport cost "
            "for all travelers."
        ),
    )

class SearchTransportResult(BaseModel):
    origin: str
    destination: str
    options: list[TransportOption]


class SearchHotelsInput(BaseModel):
    destination: str = Field(
        ...,
        min_length=1,
        description="The destination where accommodation is required.",
    )


class HotelOption(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
    )

    total_price: int = Field(
        ...,
        ge=0,
        description=(
            "The total accommodation cost "
            "for the complete stay."
        ),
    )

class SearchHotelsResult(BaseModel):
    destination: str
    options: list[HotelOption]

class CalculateTripCostInput(BaseModel):
    transport_total_price: int = Field(
        ...,
        gt=0,
        description=(
            "The selected transport option's total price. "
            "Must come from an observed transport search result."
        ),
    )

    hotel_total_price: int = Field(
        ...,
        gt=0,
        description=(
            "The selected hotel option's total price. "
            "Must come from an observed hotel search result."
        ),
    )


class CalculateTripCostResult(BaseModel):
    transport_total_price: int
    hotel_total_price: int
    total_trip_price: int