import csv

class EpaStation:
    def __init__(self, name, station_id, state, county, lon, lat):
        self.name = name
        self.station_id = station_id
        self.state = state
        self.county = county
        self.lon = lon
        self.lat = lat
        self.aqi_record = list()

    def __eq__(self, other):
        return self.station_id == other.station_id

    def add_aqi_record(self, date, pm10, aqi):
        if date not in self.aqi_record:
            self.aqi_record.append({date: (pm10, aqi)})


def create_station_object_list(file_name):
    station_list = list()
    with open(file_name, 'r') as file_obj:
        data = csv.reader(file_obj)
        for row in data:
            station = EpaStation(row[6], int(row[3]), row[7],
                                 row[-3], float(row[-2]), float(row[-1]))
            date, pm10, aqi = row[0], float(row[1]), int(row[2])  # adjust to your CSV
            if station in station_list:
                match = station_list[station_list.index(station)]
                match.add_aqi_record(date, pm10, aqi)
            else:
                station.add_aqi_record(date, pm10, aqi)
                station_list.append(station)
    return station_list