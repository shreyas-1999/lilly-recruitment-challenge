from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
"""
This module defines a FastAPI application for managing a list of medicines.
It provides endpoints to retrieve all medicines, retrieve a single medicine by name,
and create a new medicine.
Endpoints:
- GET /medicines: Retrieve all medicines from the data.json file.
- GET /medicines/{name}: Retrieve a single medicine by name from the data.json file.
- POST /create: Create a new medicine with a specified name and price.
- POST /update: Update the price of a medicine with a specified name.
- DELETE /delete: Delete a medicine with a specified name.
Functions:
- get_all_meds: Reads the data.json file and returns all medicines.
- get_single_med: Reads the data.json file and returns a single medicine by name.
- create_med: Reads the data.json file, adds a new medicine, and writes the updated data back to the file.
- update_med: Reads the data.json file, updates the price of a medicine, and writes the updated data back to the file.
- delete_med: Reads the data.json file, deletes a medicine, and writes the updated data back to the file.
Usage:
Run this module directly to start the FastAPI application.
"""
import uvicorn
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optimizing funtions to reduce code redundancy
def read_data():
    """
    This is a function that reads the data.json file and returns all medicines.
    Returns:
        dict: A dictionary of all medicines
    """
    try:
        with open('data.json') as meds:
            return json.load(meds)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail="Error in reading the data")

@app.get("/medicines")
def get_all_meds():
    """
    This function returns all medicines from the data.json file.
    Returns:
        dict: A dictionary of all medicines
    """
    data = read_data()
    medicines = []
    for med in data["medicines"]:
        if med['name'] not in (None, ""): # Handling missing values in the data file
            if med['price'] not in (None, ""): # Handling null price values
                medicines.append({
                    "name": med['name'],
                    "price": f"£{med['price']:.2f}" # Estimate all prices to 2 decimal points
                })
            else:
                medicines.append({
                    "name": med['name'],
                    "price": "Price Not Available"
                })
    return {"medicines": medicines}

@app.get("/medicines/{name}")
def get_single_med(name: str):
    """
    This function reads the data.json file and returns a single medicine by name.
    Args:
        name (str): The name of the medicine to retrieve.
    Returns:
        dict: A dictionary containing the medicine details
    """
    data = read_data()
    for med in data["medicines"]:
        if med['name'] == name:
            if med['price'] not in (None, ""): # Handling null price values
                return {
                "name": med['name'],
                "price": f"£{med['price']:.2f}"}
            else:
                return {
                "name": med['name'],
                "price": "Price not available"}

    # Send error response if entered medicine name is not found
    return {
            "status": "error",
            "code": "404",
            "message": "Medicine not found"}

@app.post("/create")
def create_med(name: str = Form(...), price: float = Form(...)):
    """
    This function creates a new medicine with the specified name and price.
    It expects the name and price to be provided as form data.
    Args:
        name (str): The name of the medicine.
        price (float): The price of the medicine.
    Returns:
        dict: A message confirming the medicine was created successfully.
    """
    # Send error response if user tries to create entries with null/empty values
    if name in (None, "") or price in (None, ""):
        return {
            "status": "error",
            "code": "400",
            "message": "Provide valid entries for Name and Price"}

    try:
        with open('data.json', 'r+') as meds:
            current_db = json.load(meds)
            new_med = {"name": name, "price": price}
            current_db["medicines"].append(new_med)
            meds.seek(0)
            json.dump(current_db, meds)
            meds.truncate() # Problem: Could cause issues during concurrent writes.
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail="Error in reading the data")
        
    return {"message": f"Medicine created successfully with name: {name}"}

@app.post("/update")
def update_med(name: str = Form(...), price: float = Form(...)):
    """
    This function updates the price of a medicine with the specified name.
    It expects the name and price to be provided as form data.
    Args:
        name (str): The name of the medicine.
        price (float): The new price of the medicine.
    Returns:
        dict: A message confirming the medicine was updated successfully.
    """

    if name in (None, "") or price in (None, ""):
        return {
            "status": "error",
            "code": "400",
            "message": "Provide valid entries for Name and Price"
        }

    try:
        with open('data.json', 'r+') as meds:
            current_db = json.load(meds)
            for med in current_db["medicines"]:
                if med['name'] == name:
                    med['price'] = price
                    meds.seek(0)
                    json.dump(current_db, meds)
                    meds.truncate()
                    return {"message": f"Medicine updated successfully with name: {name}"}
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail="Error in reading the data")
    # Send error response if entered medicine name is not found
    return {
        "status": "error",
        "code": "404",
        "message": "Medicine not found"
    }

@app.delete("/delete")
def delete_med(name: str = Form(...)):
    """
    This function deletes a medicine with the specified name.
    It expects the name to be provided as form data.
    Args:
        name (str): The name of the medicine to delete.
    Returns:
        dict: A message confirming the medicine was deleted successfully.
    """
    try:
        with open('data.json', 'r+') as meds:
            current_db = json.load(meds)
            for med in current_db["medicines"]:
                if med['name'] == name:
                    current_db["medicines"].remove(med)
                    meds.seek(0)
                    json.dump(current_db, meds)
                    meds.truncate()
                    return {"message": f"Medicine deleted successfully with name: {name}"}
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail="Error in reading the data")
    # Send error response if entered medicine name is not found
    return {
            "status": "error",
            "code": "404",
            "message": "Medicine not found"}

# Add your average function here
@app.get("/average_price")
def get_average_price():
    """
    This function calculate and returns the average price of all medicines.
    """
    data = read_data()
    total_price = 0
    count = 0
    for med in data["medicines"]:
        if med['price'] not in (None, ""):
            total_price += med['price']
            count += 1
    if count == 0:
        return {"average_price": "No valid prices available"}
    average_price = total_price / count
    return {"average_price": f"£{average_price:.2f}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)