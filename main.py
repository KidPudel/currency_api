from fastapi import FastAPI, Query, Depends
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


def make_proper_currency_code(currency: Annotated[str, Query(..., description="currency code like USD, EUR, etc.")]):
    currency = currency.upper()
    if currency == "RUB":
        currency == "RUR"
    return currency
    


@app.get("/currency-rate", description="get the currency rate of 'convert_to' based on 'convert_from'")
async def currency_rate_handler(
    from_currency: Annotated[str, Depends(make_proper_currency_code)], 
    to_currency: Annotated[str, Depends(make_proper_currency_code)], 
    amount: Annotated[int, Query(..., description="the amount of from_currency")]
):

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


