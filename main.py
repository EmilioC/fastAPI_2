
#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

# Iniciar proyecto
# Activar entorno virtual .\venv\Scripts\activate
# Lanzar aplicación: uvicorn main:app --reload


app = FastAPI() 

# Models
class HairColor(Enum): 
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location (BaseModel):
    city: str
    state: str
    country: str
    
class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50, 
        example = "Emilio"    
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional [HairColor] = Field (default= None)
    is_married: Optional [bool] = Field (default=None)
    
    class Config: 
         schema_extra = {
             "example": {
                 "first_name": "Facundo",
                 "last_name": "García Martoni",
                 "age": 21, 
                 "hair_color": "blonde",
                 "is_married": False
             }
        }

""" En el home vamos a ejecutar la aplicación """
@app.get("/") 
def home():
    return{"Hell":"friend"}

#Request and Respond Body

@app.post("/person/new")
# ... indica que es obligatorio
def create_person( person: Person = Body(...)): 
    return person

# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person( 
                #User no podrá enviar nunca menos de 1 y máximo 50 caracteres
        name: Optional[str] = Query (
            None, 
            min_length=1, 
            max_length=50,
            title= "Person Name",
            description="This is the person name. It's between 1 and 50 characters",
            example="Rocio"
            ),
        age: str = Query(
            ...,
            title="Person Age",
            description="This is the person age. It's required",
            example=85
            ),
        
):
    return {name: age}

# Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person Id",
        description="This is the person id. It's required",
        example=1258
        )
):
    return {person_id: "It exists¡"}

# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path (
        ..., 
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example= 21512
    ),
        person: Person = Body (...),
        location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results
