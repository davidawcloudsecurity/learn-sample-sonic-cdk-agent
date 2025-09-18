PRICES = {
    "VCE": {"min": 250},
    "BCN": {"min": 200},
    "NCE": {"min": 180},
    "PMI": {"min": 150},
    "ATH": {"min": 300},
    "SKG": {"min": 300},
    "CFU": {"min": 300},
    "HER": {"min": 300},
    "CUN": {"min": 700},
    "MIA": {"min": 500}
}

def get_air_destinations_and_respective_cheapest_prices(iOriginAirportCode: str) -> str:
    """
    Provides an array of available destinations and respective cheapest price per roundtrip passenger from an origin airport
    
    Parameters:
    - iOriginAirportCode: Origin airport code
    
    Returns:
    - List of destinations and their respective lowest prices. Prices are provided in USD.
    """
    available_destinations = []
    for destination, prices in PRICES.items():
        if destination != iOriginAirportCode:
            available_destinations.append(
                {"destination_airport_code": destination, "lowest_price": prices["min"]}
            )
    print(f"get_available_destinations_and_respective_cheapest_prices({iOriginAirportCode})={available_destinations}")
    oAvailableDestinationsAsString = str(available_destinations)
    return oAvailableDestinationsAsString
    #"\n---\n".join(available_destinations)

