# Undersea Cables Mapper 🌍

This project fetches and parses submarine cable data from [submarinecablemap.com](https://www.submarinecablemap.com) and stores it in a local SQLite database (`cables.db`). It matches cables to landing points based on geographic proximity using the haversine formula.

## Features

- Pulls live JSON data from submarinecablemap.com
- Matches cable endpoints to nearby landing points
- Stores results in SQLite for querying or visualizing

## To Run

```bash
pip install -r requirements.txt
python parse_json.py
python view_cables.py
