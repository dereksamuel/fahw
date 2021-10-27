#Python
from typing import Optional;

#Pydantic
from pydantic import BaseModel;

#FastApi
from fastapi import FastAPI;
from fastapi import Body, Query;

app = FastAPI();

#Models
class Person(BaseModel): # herencia de clases el basemodel
  first_name : str;
  last_name : str;
  age : int;
  hair_color : Optional[str] = None;
  is_married : Optional[bool] = False;
  abilities : dict = None;

@app.get("/")
def home():
  return {
    "Derek": "Es guapo",
  };

# Request and Responde Body

@app.post("/agent/create")
def new_agent(person: Person = Body(...)): # ... es obligatorio en python
  return person;

@app.get("/agent/detail")
def show_agent(
  name: Optional[str] = Query(None, min_length = 1, max_length = 50),
  age: int = Query(...), # si es obligatorio el query parameter deberia ser path parameter
):
  return {
    name: age,
  }
