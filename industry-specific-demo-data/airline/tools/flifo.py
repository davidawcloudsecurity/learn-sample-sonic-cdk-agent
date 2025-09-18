from datetime import date
def get_airline_flight_date_status(iFlightNumber: str, iDate: date):
    """
    Returns the internal status of a flight date including scheduled and actual times, progress, horizontal and vertical position, next waypoints, etc.
    Parameters:
    - flight: Flight number e.g. 7X0006
    - date: Flight date e.g. 20250601
    Returns:
    - Details about the flight date
    """
    print(iFlightNumber, iDate)
    flight_date_status = {
        "flight_number": iFlightNumber,
        "flight_date": iDate,
        #"board_point_icao": "KIAH",
        #"board_point_iata": "IAH",
        #"off_point_icao": "EGLL",
        #"off_point_iata": "LHR",
        "scheduled_departure_time": "06:00",
        "scheduled_arrival_time": "08:00",
        "actual_departure_time": "06:15",
        "actual_arrival_time": "08:15",
        "status": "in flight",
        "progress": 0.5,
        #"current_airspace": "KFFF",
        #"vertical_fl": 320
    }
    print(f"get_flight_date_status({iFlightNumber}, {iDate})={flight_date_status}")
    oFlightDateStatusAsString = str(flight_date_status)
    return oFlightDateStatusAsString
