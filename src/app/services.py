import io

import numpy as np
import piq
import torch
from PIL import Image

__all__ = ("get_brisque_score", "get_ms_ssim_score")


async def get_brisque_score(image_bytes: bytes) -> float:
    """
    Get the BRISQUE score of an image (bytes)
    Code references: https://github.com/photosynthesis-team/piq/blob/master/examples/image_metrics.py
    :param image_bytes:
    :return: BRISQUE score
    """
    # converting bytes to torch tensor
    image = Image.open(io.BytesIO(image_bytes)).convert("L")
    # Convert to tensor from 1 to 255
    image_tensor = torch.tensor(np.array(image)).unsqueeze(0).unsqueeze(0) / 255.0

    if torch.cuda.is_available():
        # Move to GPU to make computaions faster
        image_tensor = image_tensor.cuda()

    return piq.brisque(image_tensor, data_range=1.0, reduction="none").item()


async def get_ms_ssim_score(original_image_bytes: bytes, distorted_image_bytes: bytes) -> float:
    """
    Get the MS-SSIM score of two images (bytes)
    Code references: https://github.com/photosynthesis-team/piq/blob/master/examples/image_metrics.py
    :param original_image_bytes:
    :param distorted_image_bytes:
    :return: MS-SSIM score
    """

    original_image = Image.open(io.BytesIO(original_image_bytes)).convert("RGB")
    distorted_image = Image.open(io.BytesIO(distorted_image_bytes)).convert("RGB")

    original_image_tensor = (
        torch.tensor(np.array(original_image)).permute(2, 0, 1).unsqueeze(0) / 255.0
    )
    distorted_image_tensor = (
        torch.tensor(np.array(distorted_image)).permute(2, 0, 1).unsqueeze(0) / 255.0
    )

    if torch.cuda.is_available():
        original_image_tensor = original_image_tensor.cuda()
        distorted_image_tensor = distorted_image_tensor.cuda()

    ms_ssim_index: torch.Tensor = piq.multi_scale_ssim(
        original_image_tensor, distorted_image_tensor, data_range=1.0
    )
    return ms_ssim_index.item()
