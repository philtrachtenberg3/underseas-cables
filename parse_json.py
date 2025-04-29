import json
import sqlite3
from math import radians, sin, cos, sqrt, atan2
import os
import requests

def load_json_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def haversine(coord1, coord2):
    # Approximate Earth radius in kilometers
    R = 6371.0
    lon1, lat1 = map(radians, coord1)
    lon2, lat2 = map(radians, coord2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c  # distance in km

def build_cable_landing_map(cables, landing_points, threshold_km=10):
    cable_endpoints = []

    # Build a list of (cable_name, endpoint_coord)
    for cable in cables['features']:
        name = cable['properties']['name']
        for segment in cable['geometry']['coordinates']:
            cable_endpoints.append((name, segment[0]))      # start of segment
            cable_endpoints.append((name, segment[-1]))     # end of segment

    matches = []
    for lp in landing_points['features']:
        lp_name = lp['properties']['name']
        lp_coord = lp['geometry']['coordinates']

        for cable_name, cable_coord in cable_endpoints:
            if haversine(lp_coord, cable_coord) < threshold_km:
                matches.append((cable_name, lp_name))

    return matches

def parse_and_store(cables, landing_points):
    matches = build_cable_landing_map(cables, landing_points)

    if not os.path.exists('cables.db'):
        conn = sqlite3.connect('cables.db')
        c = conn.cursor()
        c.execute('CREATE TABLE cables (name TEXT, landing_point TEXT)')
        conn.commit()
    else:
        conn = sqlite3.connect('cables.db')
        c = conn.cursor()

    for cable, location in matches:
        c.execute('INSERT INTO cables (name, landing_point) VALUES (?, ?)', (cable, location))

    conn.commit()
    conn.close()
    print(f"Saved {len(matches)} cable-to-landing-point entries.")

if __name__ == "__main__":
    cables = load_json_from_url("https://www.submarinecablemap.com/api/v3/cable/cable-geo.json")
    landing_points = load_json_from_url("https://www.submarinecablemap.com/api/v3/landing-point/landing-point-geo.json")
    parse_and_store(cables, landing_points)
