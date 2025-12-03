from pathlib import Path
import torch
import os

def load_yolo(which):
    """Load a YOLO network from local repository. Download the weights there if needed."""

    cwd = Path.cwd()
    yolo_dir = str(Path(__file__).parent.joinpath("yolov5"))
    os.chdir(yolo_dir)

    # Patch để PyTorch >=2.6 load checkpoint YOLOv5
    from detection.yolov5.models.yolo import Model
    torch.serialization.add_safe_globals([Model])

    # Load model bình thường
    model = torch.hub.load(yolo_dir, which, source="local", trust_repo=True)

    os.chdir(str(cwd))
    return model
