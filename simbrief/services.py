import requests


class SimBriefService:
    BASE_URL = "https://www.simbrief.com/api/xml.fetcher.php"
    TIMEOUT = 10

    @staticmethod
    def fetch_latest_flight(pilot_id):
        response = requests.get(
            SimBriefService.BASE_URL,
            params={"userid": pilot_id, "json": 1},
            timeout=SimBriefService.TIMEOUT
        )
        data = response.json()
        return {
            "origin": data["origin"]["icao_code"],
            "destination": data["destination"]["icao_code"],
            "alternate": data["alternate"]["icao_code"],
            "aircraft": data["aircraft"]["icaocode"],
            "block_fuel": float(data["fuel"]["plan_ramp"]),
            "trip_fuel": float(data["fuel"]["enroute_burn"]),
            "flight_level": int(data["general"]["initial_altitude"]),
            "cost_index": int(data["general"]["costindex"]),
            "route": data["general"]["route"],
            "passengers": int(data["weights"]["pax_count"]),
            "departure_time": data["times"]["sched_out"],
        }
