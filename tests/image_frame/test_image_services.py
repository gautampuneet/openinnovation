from src.image_processor.services.image_frame_service import ImageService
from ..constants import Constants

def test_process_csv(db):
    with open("data/img.csv") as file:
        csv_data = file.read()
        image_service = ImageService()
        file_id = image_service.process_csv(csv_data)
        assert isinstance(file_id, str)

def test_get_image_frames():
    image_service = ImageService()
    depth_min = 9000.1
    depth_max = 9000.2
    frames = image_service.get_image_frames(depth_min, depth_max,file_id=Constants.csv_file_id)
    assert isinstance(frames, list)

