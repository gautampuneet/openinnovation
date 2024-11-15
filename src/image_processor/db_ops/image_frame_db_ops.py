import uuid
import pickle
from typing import List
from sqlalchemy.orm import Session
from src.image_processor.models.image_frame import ImageFrame

class ImageFrameOps:
    def __init__(self, db: Session):
        self.db = db

    def insert_image_frame(self, depth: float, pixels: bytes, file_id: str = str(uuid.uuid4())) -> None:
        """
            Inserts a single image frame into the database.

            Args:
                depth (float): The depth value associated with the frame.
                pixels (bytes): The serialized pixel data.
                file_id (str, optional): A unique identifier for the file. Defaults to a new UUID.

            Returns:
                None
        """
        image_frame = ImageFrame(depth=depth, pixels=pixels, file_id=file_id)
        self.db.add(image_frame)
        self.db.commit()

    def bulk_insert_image_frame(self, image_frames: List[ImageFrame]) -> None:
        self.db.add_all(image_frames)
        self.db.commit()

    def get_image_frames(self, depth_min: float, depth_max: float, file_id: str) -> List[ImageFrame]:
        """
            Fetches image frames from the database within a specified depth range and file ID.

            Args:
                depth_min (float): The minimum depth value.
                depth_max (float): The maximum depth value.
                file_id (str): The unique file ID associated with the frames.

            Returns:
                List[ImageFrame]: A list of ImageFrame objects with deserialized pixel data.
        """
        result_data = self.db.query(ImageFrame
                                    ).filter(ImageFrame.depth >= depth_min,
                                             ImageFrame.depth <= depth_max, ImageFrame.file_id.__eq__(file_id)
                                             ).all()
        for frame in result_data:
            retrieved_pixels_array = pickle.loads(frame.pixels)
            retrieved_pixels_array = retrieved_pixels_array.tolist()
            frame.pixels = retrieved_pixels_array
        return result_data
    
    