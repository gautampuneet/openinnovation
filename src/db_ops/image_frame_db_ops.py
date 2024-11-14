import pickle
from sqlalchemy.orm import Session
from src.models.image_frame import ImageFrame
import uuid

class ImageFrameOps:
    def __init__(self, db: Session):
        self.db = db

    def insert_image_frame(self, depth: float, pixels: bytes, file_id: str = str(uuid.uuid4())):
        image_frame = ImageFrame(depth=depth, pixels=pixels, file_id=file_id)
        self.db.add(image_frame)
        self.db.commit()

    def bulk_insert_image_frame(self, image_frames):
        self.db.add_all(image_frames)
        self.db.commit()

    def get_image_frames(self, depth_min: float, depth_max: float, file_id: str):
        result_data = self.db.query(ImageFrame
                                    ).filter(ImageFrame.depth >= depth_min,
                                             ImageFrame.depth <= depth_max, ImageFrame.file_id.__eq__(file_id)
                                             ).all()
        for frame in result_data:
            retrieved_pixels_array = pickle.loads(frame.pixels)
            retrieved_pixels_array = retrieved_pixels_array.tolist()
            frame.pixels = retrieved_pixels_array
        return result_data
    
    