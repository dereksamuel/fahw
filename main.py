#Python
from enum import Enum;
from typing import Any, Dict, Optional;

#Pydantic
from pydantic import BaseModel, Field, IPvAnyAddress;
from pydantic.networks import EmailStr, HttpUrl;

#FastApi
from fastapi import FastAPI;
from fastapi import Body, Query, Path

app = FastAPI();

#Models

class HairColor(Enum):
  white = "White".lower();
  brown = "Brown".lower();
  black = "Black".lower();
  blonde = "Blonde".lower();
  red = "Red".lower();

class Agent(BaseModel): # herencia de clases el basemodel
  first_name: str = Field(
    ...,
    min_length = 1,
    max_length = 50,
    example = "Derek Samuel Miguel"
  );
  last_name: str = Field(
    ...,
    min_length = 1,
    max_length = 50,
    example = "Ponche"
  );
  age: int = Field(
    ...,
    gt = 0,
    le = 120,
    example = 25
  );
  email: EmailStr = Field(...);
  addressIp: Optional[IPvAnyAddress] = Field(...);
  website_url: Optional[HttpUrl] = Field(...);
  hair_color: Optional[HairColor] = Field(
    default = None,
    example = "blonde"
  );
  is_married: Optional[bool] = Field(default = False);
  abilities: Optional[Dict[str, Any]] = Field(default = None);
  # class Config():
  #   schema_extra = {
  #     "example": {
  #       "first_name": "Derek Samuel",
  #       "last_name": "Paul Pena",
  #       "age": 18,
  #       "email": "dereksamuelgr@gmail.com",
  #       "addressIp": "192.168.5.111",
  #       "website_url": "https://platzi.com/clases/2513-fastapi/41909-creando-ejemplos-de-request-body-automaticos/",
  #       "hair_color": "blonde",
  #       "is_married": False,
  #       "abilities": {
  #         "draw": True,
  #         "guapo": True,
  #         "fight with her self": True,
  #       }
  #     },
  #   };

class Location(BaseModel):
  city: str = Field(
    ...,
    min_length = 0,
    example = "Bogota"
  );
  lat: Optional[float] = Field(
    default = None,
    example = 0.5
  ); # latitud
  lon: Optional[float] = Field(
    default = None,
    example = 0.598333
  ); # longitud
  country: Optional[str] = Field(
    default = None,
    example = "Colombia"
  );

@app.get("/")
def home():
  return {
    "Derek": "Es guapo",
  };

# Request and Responde Body

@app.post("/agent/create")
def new_agent(person: Agent = Body(...)): # ... es obligatorio en python
  return person;

@app.get("/agent/detail")
def show_agent(
  name: Optional[str] = Query(
    None,
    min_length = 1,
    max_length = 50,
    title = "Agent Name",
    description = "This is the agent name(very secret). It's between 1 and 50 characters",
    example = "Juan",
  ),
  age: int = Query(
    ...,
    title = "Agent age",
    description = "This is the agent AGE. This parameter is required because we need know the age(18 years old)",
    example = 19,
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
    example = 123,
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
    example = 123,
  ),
  new_agent: Agent = Body(...),
  location: Location = Body(...),
):
  results = new_agent.dict(); # agent to dict
  results.update(location.dict()); # combinar dos diccionarios
  # # no x & z pues fastapi no soporta todavia todo esto

  return {
    "status": "UPDATED",
    "data": results,
    "new_agent": new_agent,
    "ID": agent_id,
  };
