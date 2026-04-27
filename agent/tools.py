"""Tool definitions for the StayEase AI agent."""

from langchain_core.tools import tool
from pydantic import BaseModel, Field


# --- Input Schemas ---

class SearchPropertiesInput(BaseModel):
    """Input schema for searching available properties."""

    location: str = Field(description="City or area in Bangladesh, e.g. Cox's Bazar")
    check_in: str = Field(description="Check-in date in YYYY-MM-DD format")
    check_out: str = Field(description="Check-out date in YYYY-MM-DD format")
    guests: int = Field(description="Number of guests")


class GetListingDetailsInput(BaseModel):
    """Input schema for getting details of a specific listing."""

    listing_id: int = Field(description="Unique ID of the listing")


class CreateBookingInput(BaseModel):
    """Input schema for creating a booking."""

    listing_id: int = Field(description="Unique ID of the listing to book")
    guest_name: str = Field(description="Full name of the guest")
    check_in: str = Field(description="Check-in date in YYYY-MM-DD format")
    check_out: str = Field(description="Check-out date in YYYY-MM-DD format")
    guests: int = Field(description="Number of guests")


# --- Tools ---

@tool("search_available_properties", args_schema=SearchPropertiesInput)
def search_available_properties(
    location: str,
    check_in: str,
    check_out: str,
    guests: int,
) -> list[dict]:
    """Search for available properties by location, dates, and guest count.

    Queries the listings table for properties that match the location,
    can accommodate the number of guests, and have no conflicting bookings
    for the given date range.
    """
    # TODO: Replace with actual PostgreSQL query
    # Example:
    #   SELECT id, name, location, price_per_night, rating, max_guests
    #   FROM listings
    #   WHERE location ILIKE %s
    #     AND max_guests >= %s
    #     AND is_available = TRUE
    #     AND id NOT IN (
    #       SELECT listing_id FROM bookings
    #       WHERE check_in < %s AND check_out > %s
    #     )
    return [
        {
            "listing_id": 1,
            "name": "Sea Pearl Hotel",
            "location": "Cox's Bazar",
            "price_per_night": 4500.00,
            "rating": 4.5,
            "max_guests": 4,
        },
        {
            "listing_id": 2,
            "name": "Ocean View Resort",
            "location": "Cox's Bazar",
            "price_per_night": 6200.00,
            "rating": 4.8,
            "max_guests": 3,
        },
    ]


@tool("get_listing_details", args_schema=GetListingDetailsInput)
def get_listing_details(listing_id: int) -> dict:
    """Get full details for a specific listing by its ID.

    Queries the listings table and returns all information including
    description and amenities.
    """
    # TODO: Replace with actual PostgreSQL query
    # SELECT * FROM listings WHERE id = %s
    return {
        "listing_id": listing_id,
        "name": "Sea Pearl Hotel",
        "location": "Cox's Bazar",
        "description": "Beachfront hotel with stunning Bay of Bengal views.",
        "price_per_night": 4500.00,
        "rating": 4.5,
        "max_guests": 4,
        "amenities": ["WiFi", "AC", "Breakfast", "Pool", "Parking"],
    }


@tool("create_booking", args_schema=CreateBookingInput)
def create_booking(
    listing_id: int,
    guest_name: str,
    check_in: str,
    check_out: str,
    guests: int,
) -> dict:
    """Create a new booking for a guest.

    Inserts a row into the bookings table and returns the booking
    confirmation with total price.
    """
    # TODO: Replace with actual PostgreSQL insert
    # 1. Fetch price_per_night from listings WHERE id = listing_id
    # 2. Calculate total = price_per_night * number_of_nights
    # 3. INSERT INTO bookings (...) VALUES (...)
    # 4. Return confirmation
    return {
        "booking_id": 101,
        "listing_name": "Sea Pearl Hotel",
        "total_price": 9000.00,
        "status": "confirmed",
    }