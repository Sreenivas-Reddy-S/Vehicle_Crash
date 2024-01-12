import json

import uvicorn
from bson import ObjectId
from fastapi import FastAPI
from folium.plugins import MarkerCluster
from flask import Flask, jsonify, request, redirect, url_for
from pymongo import MongoClient
from flask_cors import CORS
from math import cos, sin, asin, sqrt
from math import radians
import re
import folium
import pandas as pd
import numpy as np
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# app = Flask(__name__)
app = FastAPI()
# CORS middleware configuration
origins = ["*"]  # Replace "*" with your front-end URL(s) in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB setup
connection_string = 'mongodb+srv://cardio1697:Root123@cluster0.o1uhh6a.mongodb.net/Cardio_Test?tlsCAFile=cacert.pem'
client = MongoClient(connection_string)
db = client['Car_Crash']
car_crash_collection = db['car_crash_collection']


# Create a custom JSON encoder that handles ObjectId
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)


def convert_data_to_string(data):
    for key, value in data.items():
        data[key] = str(value)
    return data


def convert_float_to_str(obj):
    if isinstance(obj, float) and (abs(obj) > 1e308 or abs(obj) < 1e-308):
        return str(obj)
    return obj


@app.get("/retrieve_records_by_agency/{agency_name}")
def retrieve_records_by_agency(agency_name: str):
    try:
        # Define the query to retrieve records where the "Agency Name" contains the given string
        query = {
            'Agency Name': {'$regex': f'.*{agency_name}.*', '$options': 'i'}}  # 'i' option makes it case-insensitive

        # Retrieve the records using the query
        records = list(car_crash_collection.find(query))

        # Convert all data to strings
        formatted_records = [convert_data_to_string(record) for record in records]

        return formatted_records
    except Exception as e:
        return {"error": str(e)}


@app.get("/retrieve_records_by_ACRS_Report_Type/{acsr_type}")
def retrieve_records_by_ACRS_Report_Type(acsr_type: str):
    try:
        # Define the query to retrieve records by ACRS Report Type
        query = {'ACRS Report Type': acsr_type}

        # Retrieve the records using the query
        records = list(car_crash_collection.find(query))

        # Convert all data to strings
        formatted_records = [convert_data_to_string(record) for record in records]

        return formatted_records
    except Exception as e:
        return {"error": str(e)}


@app.get("/retrieve_records_by_crash_date_and_time/{crash_date_time:path}")
def retrieve_records_by_crash_date_and_time(crash_date_time: str):
    try:
        # Define a regex pattern to match the date and time format (e.g., '05/31/2019 03:00:00 PM')
        regex_pattern = f'.*{re.escape(crash_date_time)}.*'

        # Modify the regex pattern based on the actual date and time format in your data

        query = {'Crash Date/Time': re.compile(regex_pattern, re.IGNORECASE)}

        # Retrieve the records using the query
        records = list(car_crash_collection.find(query))

        # Convert all data to strings
        formatted_records = [convert_data_to_string(record) for record in records]

        return formatted_records
    except Exception as e:
        return f"Error: {str(e)}"


@app.get("/retrieve_records_by_Person_ID/{person_id}")
def retrieve_records_by_Person_ID(person_id: str):
    try:
        # Define the query to retrieve records by Person ID
        query = {'Person ID': person_id}

        # Retrieve the records using the query
        records = list(car_crash_collection.find(query))

        # Convert all data to strings
        formatted_records = [convert_data_to_string(record) for record in records]

        return formatted_records
    except Exception as e:
        return f"Error: {str(e)}"


@app.get("/retrieve_records_by_vehicle_id/{vehicle_id}")
def retrieve_records_by_vehicle_id(vehicle_id: str):
    try:
        # Define the query to retrieve records by Vehicle ID
        query = {'Vehicle ID': vehicle_id}

        # Retrieve the records using the query
        records = list(car_crash_collection.find(query))

        # Convert all data to strings
        formatted_records = [convert_data_to_string(record) for record in records]

        # Move jsonify inside the request handler
        return formatted_records
    except Exception as e:
        # Also move jsonify here if you want to return the error as JSON
        return f"Error: {str(e)}"


@app.get("/retrieve_crash_records_by_weather/{weather}")
def retrieve_crash_records_by_weather(weather: str):
    try:
        # Define the query to retrieve records by weather
        query = {'Weather': weather}

        # Retrieve the records using the query
        records = list(car_crash_collection.find(query))

        # Convert all data to strings
        formatted_records = [convert_data_to_string(record) for record in records]

        return formatted_records
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


@app.get("/retrieve_crash_records_by_traffic_violation/{traffic_violation}")
def retrieve_crash_records_by_traffic_violation(traffic_violation: str):
    try:
        # Define the query to retrieve records by traffic violation
        query = {'Traffic Control': traffic_violation}

        # Retrieve the records using the query
        records = list(car_crash_collection.find(query))

        # Convert all data to strings.
        formatted_records = [convert_data_to_string(record) for record in records]

        return formatted_records
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}


@app.get("/retrieve_records_by_make_and_model/{vehicle_make}/{vehicle_model}")
def retrieve_records_by_make_and_model(vehicle_make, vehicle_model):
    try:
        # Define the query to retrieve records by vehicle make and model
        query = {
            '$and': [
                {'Vehicle Make': vehicle_make},
                {'Vehicle Model': vehicle_model},
            ]
        }

        # Retrieve the records using the query
        records = list(car_crash_collection.find(query))

        # Convert all data to strings.
        formatted_records = [convert_data_to_string(record) for record in records]

        return formatted_records
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.get("/retrieve_records_by_vehicle/{vehicle_make}/{vehicle_model}/{vehicle_year}")
def retrieve_records_by_vehicle(vehicle_make: str, vehicle_model: str, vehicle_year: str):
    try:
        # Define the query to retrieve records by vehicle make, model, and year
        query = {
            '$or': [
                {'Vehicle Make': vehicle_make},
                {'Vehicle Model': vehicle_model},
                {'Vehicle Year': vehicle_year}
            ]
        }

        # Retrieve the records using the query
        records = list(car_crash_collection.find(query))

        # Convert all data to strings
        formatted_records = [convert_data_to_string(record) for record in records]

        return formatted_records
    except Exception as e:
        return f"An error occurred: {str(e)}"


@app.get("/retrieve_records_by_latitude_and_longitude/{latitude}/{longitude}")
def retrieve_records_by_latitude_and_longitude(latitude, longitude):
    # convert latitude and longitude to double.
    latitude = float(latitude)
    longitude = float(longitude)

    try:
        # Define the query to retrieve records by Person ID
        query = {
            '$and': [
                {'Latitude': latitude},
                {'Longitude': longitude},
            ]
        }

        # Retrieve the records using the query
        records = list(car_crash_collection.find(query))

        # Convert all data to strings
        formatted_records = [convert_data_to_string(record) for record in records]

        print(records)
        return formatted_records
    except Exception as e:
        return f"Error: {str(e)}"


@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI app!"}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8005)

