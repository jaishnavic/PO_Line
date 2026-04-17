from pydantic import BaseModel

class POLineRequest(BaseModel):
    POHeaderID: str
    LineNumber: int
    LineType: str
    Category: str
    Description: str
    Quantity: float
    Price: float
    UOM: str