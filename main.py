from fastapi import FastAPI, Query
from typing import Annotated

import aiohttp


app = FastAPI()


@app.get("/")
def root():
    return {
        "status": "alive",
        "info": "call /docs to see the documentation"
    }


@app.get("/currency-rate", description="get the currency rate of 'convert_to' based on 'convert_from'")
async def currency_rate_handler(
    from_currency: Annotated[str | None, Query(description="your currency you want to convert from")] = None, 
    to_currency: Annotated[str | None, Query(description="currency you want to get value of")] = None, 
    amount: Annotated[int | None, Query(description="the amount of from_currency")] = None
):
    if from_currency == None or to_currency == None or amount == None:
        return {
            "success": False,
            "error_msg": "you must provide both sides, from_currency and to_currency, as well as amount"
        }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://cash.rbc.ru/cash/json/converter_currency_rate/?currency_from={from_currency}&currency_to={to_currency}&source=cbrf&sum={amount}&date=") as currency_response:
            json = await currency_response.json()
            return {
                "success": True,
                "currency_rate": json
            }
