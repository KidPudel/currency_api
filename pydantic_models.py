from pydantic import BaseModel

class CurrencySumModel(BaseModel):
    sum_result: float

class CurrencyModel(BaseModel):
    status: int
    data: CurrencySumModel | None

