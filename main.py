#Python
from typing import Optional;

#Pydantic
from pydantic import BaseModel;

#FastApi
from fastapi import FastAPI;
from fastapi import Body;

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
  # if (len(person["first_name"]))
  return person;
