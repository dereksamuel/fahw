from fastapi import FastAPI;

app = FastAPI();

@app.get("/")
def home():
  return {
    "Derek": "Es guapo",
  };


@app.get("/agent/{agent_id}")
def agentId():
  return {
    "Derek": "Es guapo ID Id",
  };
