from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from database import get_rooms
from services.orchestrator import analyze_hospital_room

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/images")
def read_rooms():
    try:
        return {"success": True, "data": get_rooms()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/rooms/{room_id}/analyze")
def analyze_room_endpoint(room_id: str):
    try:
        target_id = room_id.removeprefix("room-")

        rooms = get_rooms()

        room = next(
            (
                item for item in rooms
                if str(item.get("room_number", item.get("image_id", "")))
                == target_id
            ),
            None,
        )

        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")

        image_url = room.get("url") or room.get("image_url")
        if not image_url:
            raise HTTPException(
                status_code=422,
                detail="This room has no image URL",
            )

        result = analyze_hospital_room(image_url)

        return {
            "success": True,
            "room_id": room_id,
            "result": result,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def home():
    return {"message": "FastAPI is running!"}
