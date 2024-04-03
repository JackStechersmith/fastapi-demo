#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import requests
import boto3
import os
import MySQLdb
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

DBHOST = os.environ.get('DBHOST')
DBUSER = os.environ.get('DBUSER')
DBPASS = os.environ.get('DBPASS')
DB = "svc8ft"

# The URL for this API has a /docs endpoint that lets you see and test
# your various endpoints/methods.


# The zone apex is the 'default' page for a URL
# This will return a simple hello world via GET method.
@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "World Wide Web"}

@app.get("/github/repos/{user}")
def github_user_repose(user):
    url = "https://api.github.com/users/" + user + "/repos"
    response = requests.get(url)
    body = json.loads(response.text)
    return {"repos": body}

@app.get("/artistry/{anything}")
def best_artist(anything):
    return {'best artist': 'daft punk'}

@app.get("/food/{anything}")
def best_food(anything):
    return {'best food': 'pizza'}

@app.get("/whatlabisthis/{anything}")
def this_lab(anything):
    return {'this is': 'lab 6'}

# Endpoints and Methods
# /blah - endpoint
# GET/POST/DELETE/PATCH - methods
# 
# Simple GET method demo
# Adds two integers as PATH parameters
@app.get("/add/{number_1}/{number_2}")
def add_me(number_1: int, number_2: int):
    sum = number_1 + number_2
    return {"sum": sum}

# Let's develop a new one:
@app.get("/divide/{number_1}/{number_2}")
def divide_me(number_1: int, number_2: int):
    division = number_1 / number_2
    return {"division": division}


## Parameters
# Introduce parameter data types and defaults from the Optional library
@app.get("/items/{item_id}")
def read_items(item_id: int, q: str = None, s: str = None):
    # to-do: could be used to read from/write to database, use item_id as query parameter
    # and fetch results. The q and s URL parameters are optional.
    # - database
    # - flat text
    # - another api (internal)
    # - another api (external)
    return {"item_id": item_id, "q": q, "s": s}

## Data Modeling
# Model data you are expecting.
# Set defaults, data types, etc.
#
# Imagine the JSON below as a payload via POST method
# The endpoint can then parse the data by field (name, description, price, tax)
# {
#     "name":"Trek Domaine 5000",
#     "description": "Racing frame",
#     "price": 7200,
#     "tax": 381
# }

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# Start using the "Item" BaseModel
# Post / Delete / Patch methods
@app.post("/items/{item_id}")
def add_item(item_id: int, item: Item):
    return {"item_id": item_id, "item_name": item.name}

@app.delete("/items/{item_id}")
def delete_item(item_id: int, item: Item):
    return {"action": "deleted", "item_id": item_id}

@app.patch("/items/{item_id}")
def patch_item(item_id: int, item: Item):
    return {"action": "patch", "item_id": item_id}


# Use another library to make an external API request.
# An API within an API!
# https://api.github.com/users/garnaat/repos


# Incorporate with boto3: simpler than the `requests` library:
@app.get("/aws/s3")
def fetch_buckets():
     s3 = boto3.client("s3")
     response = s3.list_buckets()
     buckets = response['Buckets']
     return {"buckets": buckets}

@app.get("/albums")
def get_albums():
     db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)
     cursor = db.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute("""SELECT * FROM albums ORDER BY name""")
     results = cursor.fetchall()
     db.close()
     return results

@app.get("/albums/{id}")
def get_albums(id):
     db = MySQLdb.connect(host=DBHOST, user=DBUSER, passwd=DBPASS, db=DB)
     cursor = db.cursor(MySQLdb.cursors.DictCursor)
     cursor.execute("SELECT * FROM albums WHERE id=" + id)
     results = cursor.fetchall()
     db.close()
     return results
