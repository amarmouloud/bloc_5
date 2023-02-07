import mlflow 
import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List, Union
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import RedirectResponse


description = """

# Car rental price predictor

Use the */predict* endpoint to find the rental price per day based on your car car characteristics. 
"""


app = FastAPI(
    title="Rental car price API",
    description=description,
    version="0.1"
)

class Car(BaseModel):
    model_key: Literal['Citroën', 'Peugeot', 'Renault', 'Audi', 'BMW', 'Mercedes', 'Volkswagen', 'Mitsubishi', 'Nissan', 'Toyota', 'Other'] 
    mileage: int
    engine_power: int
    fuel: Literal['diesel', 'petrol', 'hybrid_petrol', 'electro']
    paint_color: Literal['black', 'grey', 'white', 'red', 'silver', 'blue','brown', 'Other']
    car_type: Literal['convertible', 'coupe', 'estate', 'hatchback', 'sedan', 'subcompact', 'suv', 'van']
    private_parking_available: bool
    has_gps: bool
    has_air_conditioning: bool
    automatic_car: bool
    has_getaround_connect: bool
    has_speed_regulator: bool
    winter_tires: bool


@app.get("/", include_in_schema=False)
async def redirect():
    return RedirectResponse(url='/docs')

@app.post("/predict")
async def predict(car: Car):
    """
    Prediction of salary for a given year of experience! 
    """
    # Read data
    
    input_features = pd.DataFrame(car.dict(), index=[0])
    
    # Log model from mlflow 
    logged_model = 'runs:/9dcdc76e1efd4ee89b072d58824d930f/pricing-optimization'

    # Load model as a PyFuncModel.
    loaded_model = mlflow.pyfunc.load_model(logged_model)
    print(type(loaded_model))
    prediction = loaded_model.predict(input_features)
   
    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response
if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)