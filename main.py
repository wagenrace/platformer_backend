import os

from fastapi import FastAPI
from pydantic import BaseModel

from py2neo import Graph

neo4j_url = os.environ.get("neo4jUrl")
user = os.environ.get("user")
pswd = os.environ.get("pswd")

graph = Graph(neo4j_url, auth=(user, pswd))


app = FastAPI()


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
        MATCH (cur_level:Level {number: $level_number}) 
        OPTIONAL MATCH (cur_level)-[:RED_DOOR]-(red_level)
        OPTIONAL MATCH (cur_level)-[:GREEN_DOOR]-(green_level)
        OPTIONAL MATCH (cur_level)-[:BLUE_DOOR]-(blue_level)
        
        RETURN cur_level, red_level, green_level, blue_level
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
