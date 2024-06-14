from fastapi import FastAPI, Query
from typing import Annotated
from pydantic_models import CurrencyModel
import json


import aiohttp

import constants


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
    if from_currency not in constants.CURRENCIES or to_currency not in constants.CURRENCIES:
        return {
            "success": False,
            "error_msg": "not available currency"
        }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://cash.rbc.ru/cash/json/converter_currency_rate/?currency_from={from_currency}&currency_to={to_currency}&source=cbrf&sum={amount}&date=") as currency_response:

            raw_json_response = await currency_response.json()
            json_str_response = json.dumps(raw_json_response)
            currency = CurrencyModel.model_validate_json(json_data=json_str_response)
            if currency.status == 200:
                return {
                    "success": True,
                    "sum": currency.data.sum_result,
                    "from": from_currency,
                    "to": to_currency
                }
            return {
                "success": False,
                "error_msg": f"status code is {currency.status}",
                "from": from_currency,
                "to": to_currency
            }
