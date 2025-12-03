from pathlib import Path
import torch
import os

def load_yolo(which):
    """Load a YOLO network from local repository. Download the weights there if needed."""

    cwd = Path.cwd()
    yolo_dir = str(Path(__file__).parent.joinpath("yolov5"))
    os.chdir(yolo_dir)

    # Thêm trust_repo=True để tránh lỗi weights_only với PyTorch >=2.6
    model = torch.hub.load(yolo_dir, which, source="local", trust_repo=True)

    os.chdir(str(cwd))
    return model
