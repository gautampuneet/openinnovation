import pickle
from sqlalchemy import Column, Integer, Float, LargeBinary, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ImageFrame(Base):
    __tablename__ = "image_frames"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(String(255))
    depth = Column(Float, index=True)
    pixels = Column(LargeBinary)

    def __init__(self, file_id, depth, pixels):
        self.file_id = file_id
        self.depth = depth
        self.pixels = pickle.dumps(pixels) 
