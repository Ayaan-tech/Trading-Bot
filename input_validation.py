from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Literal, Union

class BaseOrderInput(BaseModel):
    market: Literal["SPOT", "FUTURES"]
    symbol: str
    side: Literal["BUY", "SELL"]
    qty: float = Field(..., gt=0, description="Quantity must be greater than 0")
    
class MarketOrder(BaseOrderInput):
    type: Literal["MARKET"]
    
class LimitOrder(BaseOrderInput):
    type: Literal["LIMIT"]
    price: float = Field(..., gt=0, description="Price must be greater than 0 for LIMIT orders")
    
class StopOrder(BaseOrderInput):
    type: Literal["STOP"]
    stop_price: float = Field(..., gt=0, description="Stop price must be greater than 0 for STOP orders")    
class TwapOrder(BaseOrderInput):
    type: Literal["TWAP"]
    start_time: str
    end_time: str
    slices: int

    @field_validator("slices")
    def validate_slices(cls, v: int) -> int:
        if v < 1:
            raise ValueError("slices must be at least 1")
        return v
    
class GridOrder(BaseOrderInput):
    type: Literal["GRID"]
    lower_price: float
    upper_price: float
    levels: int

    @field_validator("levels")
    def validate_levels(cls, v: int) -> int:
        if v < 2:
            raise ValueError("levels must be at least 2 to form a grid")
        return v

OrderInput = Union[
    MarketOrder,
    LimitOrder,
    StopOrder,
    TwapOrder,
    GridOrder,
]
