from Config.settings import *
import requests , time
from langchain_core.tools import tool

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
    }, timeout=10)
    response.raise_for_status() # if the status code of response not (200-299) , the exception will be through
    json=response.json()
    token = json.get("access_token")
    if not token:
        raise ValueError("Access token missing in response")
    _TOKEN["token"] = token
    _TOKEN["expires_at"] = now + int(json.get("expires_in", 1800)) # 1800 -> 30 min
    return token

def search_flights(origin, destination, date):
    search_url=f"{Amadeus_BaseURL}/v2/shopping/flight-offers"
    token=get_access_token(Amadeus_Key,Amadeus_SecretKey)
    headers={"Authorization": f"Bearer {token}"}
    params={
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": 1,  # عدد البالغين (مطلوب)
        "currencyCode": "USD",  # اختياري: لتحديد العملة
        "max": 10  # اختياري: عدد النتائج المرجعة (الحد الأقصى 250)
    }
    response=requests.get(search_url,headers=headers,params=params,timeout=10)
    response.raise_for_status()
    return response.json()

@tool
def search_for_flights(origin : str, destination : str , date : str ) -> str:
    """
    Search for flights between two airports on a specific date using the Amadeus API.
    The tool receives:  
    - origin: Origin airport IATA code (e.g., CAI)  
    - destination: Destination airport IATA code (e.g., DXB)  
    - date: Travel date in format YYYY-MM-DD or DD/MM/YYYY  

    The tool must return well-formatted flight information in a clear and consistent structure, 
    showing each trip separately (trip-by-trip). Always include the following details for each flight:  
        ✈️ Flight 1:
        Airline: KU 546
        From: CAI → To: KWI
        Price: 194.99 USD
        ──────────────────────
        
    Important notes for the agent:  
    - Do NOT guess or fabricate flight data.  
    - Only return real results fetched from Amadeus.  
    - If no flights exist, return a clear message: “No flights found.”  
    - If an error occurs (e.g., invalid date, API error), return the error message clearly.  

    Purpose:  
    Enable the agent to fetch and present real flight offers from Amadeus in a clean, 
    organized, and professional format.
    """

    try:
        flights=search_flights(origin, destination, date)
        if "data" in flights:
            flights["data"].sort(key=lambda x:float(x["price"]["total"]))
            flights_count=len(flights["data"])
            lines = [f"Number of flights is {flights_count} \n"]
            for i,flight in enumerate(flights["data"],1):
                #--------------this method is difficult to trace the sources of errors---------------------
                # price = flight.get("price", {}).get("total", "N/A")
                # currency = flight.get("price", {}).get("currency", "USD")
                # segment = flight.get("itineraries", [{}])[0].get("segments", [{}])[0]
                # departure = segment.get("departure", {}).get("iataCode", "N/A")
                # arrival = segment.get("arrival", {}).get("iataCode", "N/A")
                # flight_num = segment.get("number", "N/A")
                # carrier = segment.get("carrierCode", "N/A")
                #----------------------------------------------------------------------------------------------------------------------------------------
                price=flight["price"]["total"]
                currency=flight["price"].get("currency", "USD") # USD is a default value if the currency attribute not exist
                departure=flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
                arrival=flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
                flight_num=flight["itineraries"][0]["segments"][0]["number"]
                carrier=flight["itineraries"][0]["segments"][0]["carrierCode"]
                lines.append(
                        f"✈️ Flight {i}:\n"
                        f"   Airline: {carrier} {flight_num}\n"
                        f"   From: {departure} → To: {arrival}\n"
                        f"   Price: {price} {currency}\n"
                        "   ──────────────────────\n"
                )
            return "\n".join(lines)
            #print("\n".join(lines)) 
        else:
            return f"No flights found from {origin} to {destination} on {date}."
            #print(f"No flights found from {origin} to {destination} on {date}.")
    except requests.exceptions.HTTPError as e:
        return f"Request failed due to an HTTP error: {e}"
        #print(f"Request failed due to an HTTP error: {e}")
    except Exception as e:
        return f"Error occurred:{e}" 
        #print(f"Error occurred:{e}" )


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


flights = search_flights("CAI","DXB","2025-12-25")
offer = flights["data"][0] 
#print("Selected offer summary:", offer.get("id", "no-id"), offer.get("price",{}).get("total"))
res = flight_offer_price(offer)
priced_offer = res["data"]["flightOffers"][0]
#print(priced_offer)
def flight_order(priced_offer,Fname,Lname,gender,BD,email,county_calling_code,phone_number,passport_num,passport_expire_date,passport_issuance_country,nationality8):
    price_url=f"{Amadeus_BaseURL}/v1/booking/flight-orders"
    token=get_access_token(Amadeus_Key,Amadeus_SecretKey)
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
    response= requests.post(price_url,json=payload,headers=headers,timeout=10)
    response.raise_for_status()
    return response.json()

birth_data="1990-01-01"
gender="MALE"
Fname="JOHN"
Lname="DOE"
email="john@example.com"
county_calling_code="20"
phone_number="01012345678"
passport_num="A12345678"
passport_expire_date="2030-01-01"
passport_issuance_country="EG"
nationality="EG"
print(flight_order(priced_offer,Fname,Lname,gender,birth_data,email,county_calling_code,phone_number,passport_num,passport_expire_date,passport_issuance_country,nationality))
