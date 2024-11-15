from src.image_processor.db_ops.image_frame_db_ops import ImageFrameOps
from tests.conftest import TestingSessionLocal
from ..constants import Constants

def test_insert_image_frame():
    with TestingSessionLocal() as db:
        repository = ImageFrameOps(db)
        depth = 1.0
        pixels = b"\xff" * 150 * 1
        repository.insert_image_frame(depth, pixels)
        assert True

def test_get_image_frames(db):
    with TestingSessionLocal() as db:
        repository = ImageFrameOps(db)
        file_id = Constants.csv_file_id
        depth_min = 9000.1
        depth_max = 9000.2
        frames = repository.get_image_frames(depth_min, depth_max,file_id)
        assert isinstance(frames, list)

