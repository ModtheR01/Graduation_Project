from Config.settings import *
import requests , time
from langchain_core.tools import tool
from Core.search_flights.s import session_state
from Core.search_flights.tools import search_for_flights

_TOKEN={"token": None,"expires_at":0} # _TOKEN -> name convention to assume it as a private var only in this file , all letter uper case because it is a constant
def get_access_token(client_id, client_secret):
    now = time.time() 
    if _TOKEN["token"] and _TOKEN["expires_at"] > now + 30:   # 30 seconds
        return  _TOKEN["token"]
    token_url = f"{Amadeus_BaseURL}/v1/security/oauth2/token"
    response = requests.post(token_url, data={
        "grant_type":"client_credentials",
        "client_id":client_id, 
        "client_secret":client_secret
    }, timeout=20)
    response.raise_for_status() # if the status code of response not (200-299) , the exception will be through
    json=response.json()
    token = json.get("access_token")
    if not token:
        raise ValueError("Access token missing in response")
    _TOKEN["token"] = token
    _TOKEN["expires_at"] = now + int(json.get("expires_in", 1800)) # 1800 -> 30 min
    return token

def flight_offer_price(offer): # This API is used to validate and confirm the flight price before booking.
    price_url=f"{Amadeus_BaseURL}/v1/shopping/flight-offers/pricing"
    token=get_access_token(Amadeus_Key,Amadeus_SecretKey)
    headers={
        "Authorization": f"Bearer {token}",  # Bearer  -> type of authentication
        "Content-Type" : "application/json"  # Type of data will be sent
        }
    # payload -> # put the selected offer in the correct format
    payload={
                "data": {
                    "type": "flight-offers-pricing",
                    "flightOffers": [offer]
                }
            }
    response= requests.post(price_url,json=payload,headers=headers,timeout=10)
    response.raise_for_status()
    return response.json()

@tool
def price_offer_by_index(index: int,Fname,Lname,gender,BD,email,county_calling_code,phone_number,passport_num,passport_expire_date,passport_issuance_country,nationality):
    """
    Book a selected flight offer using its index from the last search results.

    This tool should be called ONLY after:
    1. A flight search has been performed.
    2. The user has selected a flight offer by its index.

    The tool automatically validates the selected offer price 
    by calling the pricing endpoint before creating the booking.

    Parameters:
        index (int): The number of the flight offer chosen by the user 
        from the previously displayed search results.

        Fname (str): Passenger first name (uppercase recommended).
        Lname (str): Passenger last name.
        gender (str): Passenger gender ("MALE" or "FEMALE").
        BD (str): Passenger date of birth in YYYY-MM-DD format.
        email (str): Passenger email address.
        county_calling_code (str): Phone country calling code (e.g., "20" for Egypt).
        phone_number (str): Passenger mobile number.
        passport_num (str): Passport number.
        passport_expire_date (str): Passport expiry date in YYYY-MM-DD format.
        passport_issuance_country (str): Country issuing the passport (2-letter ISO code).
        nationality (str): Passenger nationality (2-letter ISO code).

    Returns:
        JSON response from Amadeus containing the booking confirmation 
        and PNR if the booking is successful.

    Notes:
        - The flight offer is automatically price-validated before booking.
        - If the index is invalid or no previous search exists, 
        the booking will fail.
    """
    index = int(index)  

    offers = session_state.get("last_offers")

    if not offers:
        return {"error": "No previous search found."}

    if index < 1 or index > len(offers):
        return {"error": "Invalid offer index."}

    selected_offer = offers[index - 1]

    final_price_of_offer=flight_offer_price(selected_offer)["data"]["flightOffers"][0]

    return flight(final_price_of_offer,Fname,Lname,gender,BD,email,county_calling_code,phone_number,passport_num,passport_expire_date,passport_issuance_country,nationality)


# @tool
def flight(index,Fname,Lname,gender,BD,email,county_calling_code,phone_number,passport_num,passport_expire_date,passport_issuance_country,nationality):

    price_url=f"{Amadeus_BaseURL}/v1/booking/flight-orders"
    token=get_access_token(Amadeus_Key,Amadeus_SecretKey)
    priced_offer = price_offer_by_index(index)
    headers={
        "Authorization": f"Bearer {token}",  
        "Content-Type" : "application/json"
        }
    payload={
                "data": {
                    "type": "flight-order",
                    "flightOffers": [
                    priced_offer
                    ],
                    "travelers": [
                    {
                        "id": "1",
                        "dateOfBirth": BD ,
                        "gender": gender,
                        "name": {
                        "firstName":Fname ,
                        "lastName": Lname
                        },
                        "contact": {
                        "emailAddress": email ,
                        "phones": [
                            {
                            "deviceType": "MOBILE",
                            "countryCallingCode": county_calling_code,
                            "number": phone_number
                            }
                        ]
                        },
                        "documents": [
                        {
                            "documentType": "PASSPORT",
                            "number": passport_num,
                            "expiryDate": passport_expire_date,
                            "issuanceCountry": passport_issuance_country,
                            "nationality": nationality,
                            "holder": True
                        }
                        ]
                    }
                    ]
                }
            }
    response= requests.post(price_url,json=payload,headers=headers,timeout=30)
    if response.status_code != 201:
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.text)
        return {"error": response.text}
    return response.json()





# flights = search_for_flights("CAI", "DXB", "2026-03-25")
# pricing_response = price_offer_by_index(1)
# priced_offer = pricing_response
# birth_data="1990-01-01"
# gender="MALE"
# Fname="JOHN"
# Lname="DOE"
# email="john@example.com"
# county_calling_code="20"
# phone_number="01012345678"
# passport_num="A12345678"
# passport_expire_date="2030-01-01"
# passport_issuance_country="EG"
# nationality="EG"
# print(flight_order(1,Fname,Lname,gender,birth_data,email,county_calling_code,phone_number,passport_num,passport_expire_date,passport_issuance_country,nationality))




