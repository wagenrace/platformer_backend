from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class Level(BaseModel):
    id: int


@app.post("/get_level_by_number")
async def door_mapping(level: Level) -> dict:
    if level.id == 1:
        doorMapping = {
            "DoorRed": {"level_num": 2, "level_encoded": "8CcC9DdD+"},
            "DoorGreen": {"level_num": 2, "level_encoded": "8CcC9DdD+"},
            "DoorBlue": {"level_num": 2, "level_encoded": "8CcC9DdD+"},
        }
    else:
        doorMapping = {
            "DoorRed": {"level_num": 1, "level_encoded": "8AaA9BbB+"},
            "DoorGreen": {"level_num": 1, "level_encoded": "8AaA9BbB+"},
            "DoorBlue": {"level_num": 1, "level_encoded": "8AaA9BbB+"},
        }

    return {"doorMapping": doorMapping, "id": level.id}
