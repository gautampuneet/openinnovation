from pydantic import BaseModel

class ImageFrameBase(BaseModel):
    depth: float

class ImageFrameCreate(ImageFrameBase):
    pixels: bytes

class ImageFrame(ImageFrameBase):
    id: int

    class Config:
        orm_mode = True
        