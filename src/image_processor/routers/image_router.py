from sqlite3 import IntegrityError
from fastapi import APIRouter, HTTPException, UploadFile, Query
from src.image_processor.services.image_frame_service import ImageService
from src.common.logging import logger
from src.image_processor.constants.error_messages import ImageProcessorErrorMessages
from src.image_processor.constants.common import Response

router = APIRouter()
image_service = ImageService()

@router.post("/upload/")
async def upload_and_resize(file: UploadFile):
    try:
        contents = await file.read()
        file_id = image_service.process_csv(contents.decode('utf-8'))
        return {"status": Response.IMAGE_UPLOADED, "file_id":file_id}
    except HTTPException:
        raise HTTPException(status_code=400, detail=ImageProcessorErrorMessages.UPLOADED_FILE_IS_CORRUPTED)
    except IntegrityError as e:
        logger.info(f"{ImageProcessorErrorMessages.ERROR_OCCURRED_IN_DB}, exception: {e}")
        raise HTTPException(status_code=500, detail=ImageProcessorErrorMessages.ERROR_OCCURRED_IN_DB)
    except Exception as e:
        logger.info(f"{ImageProcessorErrorMessages.INTERNAL_SERVER_ERROR}, exception: {e}")
        raise HTTPException(status_code=500, detail=ImageProcessorErrorMessages.INTERNAL_SERVER_ERROR)

@router.get("/image_frames/")
async def read_image_frames(file_id:str,
                            depth_min: float,
                            depth_max: float,
                            colored: bool = Query(False),
                            to_json: bool = True):
    frames = image_service.get_image_frames(depth_min, depth_max, file_id, colored)
    if not frames:
        raise HTTPException(status_code=404, detail=ImageProcessorErrorMessages.NO_IMAGE_FOUND_IN_DEPTH)

    if not to_json:
        # Save Data into S3 and Generate Pre signed Url for this
        saved_data = image_service.save_image_frames_into_s3(frames)
        return {"data": saved_data}
    else:
        return {"data": frames}
