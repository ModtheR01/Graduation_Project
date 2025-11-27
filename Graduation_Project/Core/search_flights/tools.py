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
        "max": 1  # اختياري: عدد النتائج المرجعة (الحد الأقصى 250)
    }
    response=requests.get(search_url,headers=headers,params=params,timeout=10)
    response.raise_for_status()
    print(response.json())
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
    • Airline and flight number  
    • Route (From → To)  
    • Price and currency  
    • Stops (or Non-stop)  
    • Duration  
    • Segments (each segment with departure/arrival times and airport codes)

    Important notes for the agent:  
    - Do NOT guess or fabricate flight data.  
    - Only return real results fetched from Amadeus.  
    - If no flights exist, return a clear message: “No flights found.”  
    - If an error occurs (e.g., invalid date, API error), return the error message clearly.  
    - The output should always be user-friendly and readable.

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





