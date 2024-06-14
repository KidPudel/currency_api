# About
This is a currency converter REST API service written in FastAPI
Developed with:
- Python 3.12.4
- FastAPI
- aiohttp
- pydantic
- selenium

> Full list is in `requirements.txt`

Devops part:
- basic NGINX configuration
- Dockerization with multi-stage build
- Hosting via Railway

> So yeah, this is actually hosted https://currencyapi-production.up.railway.app 👀


# Endpoints
Basically we should be interested in 2 things:
1. where is the converter?
2. where is the docs

## Converter
Example: https://currencyapi-production.up.railway.app/currency-rate?from_currency=RUB&to_currency=USD&amount=5000

Response:
```json
{
	"success": true,
	"sum": 56.6842,
	"from": "RUR",
	"to": "USD"
}
```

> Why returned RUR? Because that's what external server uses, but i've done some filtering and adjustments, so that it would be more convenient.
> P.S. Also it's case insensitive ;)

## Docs:
Swagger: https://currencyapi-production.up.railway.app/docs

