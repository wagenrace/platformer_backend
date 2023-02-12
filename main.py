import os

from fastapi import FastAPI
from pydantic import BaseModel

from py2neo import Graph
from fastapi.middleware.cors import CORSMiddleware

neo4j_url = os.environ.get("neo4jUrl")
user = os.environ.get("user")
pswd = os.environ.get("pswd")

graph = Graph(neo4j_url, auth=(user, pswd))


app = FastAPI()

origins = ["http://localhost:5500"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    response = graph.run(
        """
        MATCH (l:Level) RETURN count(l) as count
    """
    ).data()[0]
    return {"numberOfLevels": response["count"], "neo4jUrl": str(graph)}


class Level(BaseModel):
    id: int


@app.post("/get_level_by_number")
async def door_mapping(level: Level) -> dict:
    response = graph.run(
        """
        MATCH (CurrentLevel:Level {number: $level_number}) 
        OPTIONAL MATCH (CurrentLevel)-[:RED_DOOR]-(DoorRed)
        OPTIONAL MATCH (CurrentLevel)-[:GREEN_DOOR]-(DoorGreen)
        OPTIONAL MATCH (CurrentLevel)-[:BLUE_DOOR]-(DoorBlue)
        
        RETURN CurrentLevel, DoorRed, DoorGreen, DoorBlue
    """,
        level_number=level.id,
    ).data()[0]

    return response
    # if level.id == 1:
    #     doorMapping = {
    #         "DoorRed": {"level_num": 2, "level_encoded": "8CcC9DdD+"},
    #         "DoorGreen": {"level_num": 2, "level_encoded": "8CcC9DdD+"},
    #         "DoorBlue": {"level_num": 2, "level_encoded": "8CcC9DdD+"},
    #     }
    # else:
    #     doorMapping = {
    #         "DoorRed": {"level_num": 1, "level_encoded": "8AaA9BbB+"},
    #         "DoorGreen": {"level_num": 1, "level_encoded": "8AaA9BbB+"},
    #         "DoorBlue": {"level_num": 1, "level_encoded": "8AaA9BbB+"},
    #     }

    # return {"doorMapping": doorMapping, "id": level.id}
