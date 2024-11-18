# Microservice A: Currency Converter

## Setup
1. Clone the repo.
2. Install and Run PostgreSQL locally on computer.
3. Create a database called `currency_db`
4. Update `main.py` file using your PostgreSQL's credentials for all `user="YourUsername"` and `password="YourPassword"`
5. Run `pip install Flask psycopg2-binary` into terminal to install neccessary packages.
6. Run `python main.py` to start microservice.

## Routes
| Route | Description | Example Call | Example Return Response |
| ----- | ----------- | ------------ | ----------------------- |
| GET `/list` | Return an array of conversions | GET `/list` | `[{"from_currency": "USD", "rate": 0.85,"to_currency": "EUR"}, ...]` |
| GET `/convert` | Convert an amount in one currency to another currency | GET `/convert` with params `{"from_currency": USD, "to_currency": EUR, "amount": 100}` | `{"amount": 100,"converted_amount": 85,"from_currency":"USD", "rate": 0.85, "to_currency": "EUR"}` |
| POST `/add` | Add a new conversion  | POST `/add` with json `{"from_currency": from_curr, "to_currency": to_curr,  "rate": rate}` | `{"message": "Conversion added successfully.", "from_currency": from_currency, "to_currency": to_currency, "rate": rate}` |

## Requesting and Receiving Data

## UML Diagram