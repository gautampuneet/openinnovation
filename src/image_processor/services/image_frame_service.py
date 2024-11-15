import json
import uuid

import pandas as pd
from io import StringIO
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from typing import List, Dict, Any

from src.database import SessionLocal
from src.common.logging import logger
from src.image_processor.db_ops.image_frame_db_ops import ImageFrameOps
from src.image_processor.models.image_frame import ImageFrame
from src.image_processor.utils.image_frame_utils import ImageProcessor


class ImageService:

    def __init__(self):
        self.image_processor = ImageProcessor()

    def process_csv(self, csv_data: str) -> str:
        """
            Processes CSV data to resize pixel values and store them in the database.

            Args:
                csv_data (str): CSV data as a string.

            Returns:
                str: A unique file ID for the processed data.

            Raises:
                HTTPException: If parsing or processing the CSV data fails.
                Exception: For any unexpected errors.
        """
        db = SessionLocal()
        try:
            df = pd.read_csv(StringIO(csv_data))
            depths = df['depth'].values
            pixel_values = df.drop(columns=['depth']).values
            resized_pixel_values = self.image_processor.resize_image(pixel_values=pixel_values,
                                                                     new_width=150)

            file_id = str(uuid.uuid4())
            with db.begin():
                repository = ImageFrameOps(db)
                frames = [ImageFrame(depth=d, pixels=p, file_id=file_id) for d, p in zip(depths, resized_pixel_values)]
                repository.bulk_insert_image_frame(frames)

            logger.info(f"Successfully processed CSV data. File ID: {file_id}")
            return file_id

        except (pd.errors.ParserError, ValueError, KeyError) as e:
            logger.error(f"Error parsing CSV data: {e}")
            raise HTTPException(status_code=400, detail="Unable to parse the file")
        except IntegrityError as e:
            logger.error(f"Database integrity error: {e}")
            db.rollback()
            raise
        except Exception as e:  # Catch-all for unexpected errors
            logger.exception(f"Unexpected error: {e}")
            raise

    
    def get_image_frames(self,
                         depth_min: float,
                         depth_max: float,
                         file_id: str,
                         colored: bool = False) -> List[Dict[str, Any]]:
        """
           Fetches image frames from the database within a specified depth range.

           Args:
               depth_min (float): Minimum depth value.
               depth_max (float): Maximum depth value.
               file_id (str): Unique file ID associated with the frames.
               colored (bool, optional): Whether to apply a colormap to the pixels. Defaults to False.

           Returns:
               List[Dict[str, Any]]: A list of image frames with depth and pixel data.

           Raises:
               HTTPException: If fetching data from the database fails.
       """
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
                logger.error(f"Error Occurred: {e}")
                raise HTTPException(status_code=500,detail="Unable to fetch data from the db")

    @staticmethod
    def save_image_frames_into_s3(results: List[Dict[str, Any]]) -> str:
        """
            Saves the processed image frames into a temporary file in JSON format.

            Args:
                results (List[Dict[str, Any]]): The processed image frames.

            Returns:
                str: A success message indicating the file has been saved.

            Raises:
                Exception: For unexpected file I/O errors.
        """
        import os
        file_id = str(uuid.uuid4())
        os.makedirs(os.path.dirname(f"tmp/{file_id}.json"), exist_ok=True)
        with open(f"tmp/{file_id}.json", "w") as file:
            file.write(json.dumps(results))
        return "File saved Successfully"
            


