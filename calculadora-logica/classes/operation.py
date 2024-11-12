from pydantic import BaseModel


class Operation(BaseModel):
    formula: str