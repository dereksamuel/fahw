#Python
from enum import Enum;
from typing import Any, Dict, Optional

#Pydantic
from pydantic import BaseModel, Field, IPvAnyAddress;
from pydantic.networks import EmailStr, HttpUrl;

#FastApi
from fastapi import FastAPI;
from fastapi import status;
from fastapi import Body, Query, Path, Form, Header, Cookie;

app = FastAPI();

#Models

class HairColor(Enum):
  white = "White".lower();
  brown = "Brown".lower();
  black = "Black".lower();
  blonde = "Blonde".lower();
  red = "Red".lower();

class AgentBase(BaseModel):
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
  addressIp: Optional[IPvAnyAddress] = Field(
    ...,
    example = "127.0.0.1"
  );
  website_url: Optional[HttpUrl] = Field(
    ...,
    example = "https://platzi.com/clases/2514-fastapi-modularizacion-datos/41979-response-model/"
  );
  hair_color: Optional[HairColor] = Field(
    default = None,
    example = "blonde"
  );
  is_married: Optional[bool] = Field(default = False);
  abilities: Optional[Dict[str, Any]] = Field(default = None);

class Agent(AgentBase): # herencia de clases el basemodel
  password: str = Field(..., min_length=8);
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

class BaseLogin(BaseModel):
  username: str = Field(
    ...,
    min_length=1,
    max_length=30,
    example="dereksamuelgr@gmail.com");

@app.get(
  path="/",
  status_code=status.HTTP_200_OK
)
def home():
  return {
    "Derek": "Es guapo",
  };

# Request and Responde Body

@app.post(
  path="/agent/create",
  response_model = AgentBase,
  status_code=status.HTTP_201_CREATED)
def new_agent(person: Agent = Body(...)): # ... es obligatorio en python
  return person;

@app.get(
  path="/agent/detail",
  status_code=status.HTTP_200_OK)
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

@app.get(
  path="/agent/detail/{agent_id}",
  status_code=status.HTTP_200_OK) #encuentra el ultimo pero SIEMPRE TOMADO EL ULTIMO QUE ES IGUAL(endpoint)
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
@app.put(
  path="/agent/update/{agent_id}",
  status_code=status.HTTP_200_OK)
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

# Form
@app.post(
  path="/login",
  response_model=BaseLogin,
  status_code=status.HTTP_200_OK
)
def login(
  username: str = Form(
    ...,
    example="dereksamuelgr@gmail.com"),
  password: str = Form(...)):
  return BaseLogin(username=username);

# Cookies and Headers Parameters
@app.post(
  path="/contact",
  status_code=status.HTTP_200_OK
)
def contact(
  first_name: str = Form(
    ...,
    max_length=20,
    min_length=1,
  ),
  last_name: str = Form(
    ...,
    max_length=20,
    min_length=1,
  ),
  email: EmailStr = Form(...),
  message: str = Form(
    ...,
    min_length=20,
    max_length=250
  ),
  user_agent: Optional[str] = Header(default=None),
  ads: Optional[str] = Cookie(default=None),
):
  return user_agent;
