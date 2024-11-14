import logging
import uuid
from fastapi import HTTPException
import pandas as pd
from sqlalchemy.exc import IntegrityError

from src.database import SessionLocal
from src.db_ops.image_frame_db_ops import ImageFrameOps
from src.models.image_frame import ImageFrame
from src.utils.image_frame_utils import ImageProcessor
from io import StringIO


class ImageService:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.logger = logging.getLogger(__name__)

    def process_csv(self, csv_data: str):
        try:
            df = pd.read_csv(StringIO(csv_data))
            depths = df['depth'].values
            pixel_values = df.drop(columns=['depth']).values
            resized_pixel_values = self.image_processor.resize_image(pixel_values=pixel_values, new_width=150)

            db = SessionLocal()
            file_id = str(uuid.uuid4())
            with db.begin():
                repository = ImageFrameOps(db)
                frames = [ImageFrame(depth=d, pixels=p, file_id=file_id) for d, p in zip(depths, resized_pixel_values)]
                repository.bulk_insert_image_frame(frames)

            self.logger.info(f"Successfully processed CSV data. File ID: {file_id}")
            return file_id

        except (pd.errors.ParserError, ValueError, KeyError) as e:
            self.logger.error(f"Error parsing CSV data: {e}")
            raise HTTPException(status_code=400, detail="Unable to parse the file")
        except IntegrityError as e:
            self.logger.error(f"Database integrity error: {e}")
            db.rollback()
            raise
        except Exception as e:  # Catch-all for unexpected errors
            self.logger.exception(f"Unexpected error: {e}")
            raise

    
    def get_image_frames(self, depth_min: float, depth_max: float, file_id: str, colored: bool = False):
        with SessionLocal() as db:
            repository = ImageFrameOps(db)
            try:
                frames = repository.get_image_frames(depth_min, depth_max, file_id)

                result = []
               
                for frame in frames:
                    if colored:
                        colored_pixels = self.image_processor.apply_custom_colormap(frame.pixels)
                        result.append({"depth": frame.depth, "pixels": colored_pixels})
                    else:
                        result.append({"depth": frame.depth, "pixels": frame.pixels})
                return result
            except Exception as e:
                self.logger.error(f"Error Occurred: {e}")
                raise HTTPException(status_code=500,detail="Unable to fetch data from the db")
            


