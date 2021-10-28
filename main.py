#Python
from typing import Any, Dict, Optional;

#Pydantic
from pydantic import BaseModel;

#FastApi
from fastapi import FastAPI;
from fastapi import Body, Query, Path;

app = FastAPI();

#Models
class Person(BaseModel): # herencia de clases el basemodel
  first_name: str;
  last_name: str;
  age: int;
  hair_color: Optional[str] = None;
  is_married: Optional[bool] = False;
  abilities: Optional[Dict[str, Any]] = None;

class Location(BaseModel):
  city: str;
  lat: Optional[str] = None;
  lon: Optional[str] = None;
  country: Optional[str] = None;

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
  name: Optional[str] = Query(
    None,
    min_length = 1,
    max_length = 50,
    title = "Agent Name",
    description = "This is the agent name(very secret). It's between 1 and 50 characters",
  ),
  age: int = Query(
    ...,
    title = "Agent age",
    description = "This is the agent AGE. This parameter is required because we need know the age(18 years old)",
  ), # si es obligatorio el query parameter deberia ser path parameter
):
  return {
    name: age,
  }

#Validations query params

@app.get("/agent/detail/{agent_id}") #encuentra el ultimo pero SIEMPRE TOMADO EL ULTIMO QUE ES IGUAL(endpoint)
def show_agent(
  agent_id: int = Path(
    ...,
    gt = 0,
    title = "Agent ID",
    description = "This is the agent id(very SECRET)...",
  )
):
  return {
    agent_id: "It exists!",
  };

# Validations: Request Body
@app.put("/agent/update/{agent_id}")
def update_agent(
  agent_id: int = Path(
    ...,
    gt = 0,
    title = "Agent ID",
    description = "This is the agent ID",
  ),
  new_agent: Person = Body(...),
  location: Location = Body(...),
):
  results = new_agent.dict(); # agent to dict
  results.update(location.dict()); # combinar dos diccionarios
  # no x & z pues fastapi no soporta todavia todo esto

  return {
    "status": "UPDATED",
    "data": results,
    "ID": agent_id,
  };
