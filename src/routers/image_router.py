from sqlite3 import IntegrityError
from fastapi import APIRouter, HTTPException, UploadFile, Query
from src.services.image_frame_service import ImageService

router = APIRouter()
image_service = ImageService()

@router.post("/upload/")
async def upload_and_resize(file: UploadFile):
    try:
        contents = await file.read()
        file_id = image_service.process_csv(contents.decode('utf-8'))
        return {"status": "Images uploaded and resized successfully.","file_id":file_id}
    except HTTPException as e:
        raise HTTPException(status_code=400, detail="The file is corrupted/cannot be parsed")
    except IntegrityError as e:
        raise HTTPException(status_code=500, detail="Error occurred in the DB")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/image_frames/")
async def read_image_frames(file_id:str, depth_min: float, depth_max: float, colored: bool = Query(False)):
    frames = image_service.get_image_frames(depth_min, depth_max, file_id, colored)
    if not frames:
        raise HTTPException(status_code=404, detail="No image frames found in the given depth range")
    return frames
