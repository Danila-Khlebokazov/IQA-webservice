from fastapi import APIRouter, UploadFile, status
from fastapi.responses import Response

from .schemas import ScoreOutSchema
from .services import get_brisque_score, get_ms_ssim_score

router = APIRouter(prefix="/api/v1/iqa", tags=["api"])


@router.post(
    "/nr/brisque/",
    summary="No-reference Image Quality Assessment in the Spatial Domain (BRISQUE)",
    description="Measure IQA of image file by No-reference Image Quality Assessment in the Spatial Domain "
    "(BRISQUE), IEEE TIP, 2012.<br>If score is more than 50 means that image is highly distorted.",
    response_model=ScoreOutSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully calculated BRISQUE score",
            "content": {"application/json": {"example": {"score": 0.0}}},
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Failed to calculate BRISQUE score",
            "content": {
                "application/json": {"example": {"detail": "Failed to calculate BRISQUE score"}}
            },
        },
    },
)
async def nr_brisque(image: UploadFile):
    try:
        score = await get_brisque_score(await image.read())
        return ScoreOutSchema(score=score)
    except Exception as e:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))


@router.post(
    "/fr/ms-ssim/",
    summary="Multi-scale Structural Similarity for Image Quality Assessment (MS-SSIM), "
    "IEEE Asilomar Conference on Signals, Systems and Computers, 2003",
    description="Measure IQA of image file by Full-reference Multi-scale Structural Similarity for Image Quality "
    "Assessment (MS-SSIM), IEEE Asilomar Conference on Signals, Systems and Computers, 2003",
    response_model=ScoreOutSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {
            "description": "Successfully calculated MS-SSIM score",
            "content": {"application/json": {"example": {"score": 0.0}}},
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Failed to calculate MS-SSIM score",
            "content": {
                "application/json": {"example": {"detail": "Failed to calculate MS-SSIM score"}}
            },
        },
    },
)
async def fr_ms_ssim(original_image: UploadFile, distorted_image: UploadFile):
    try:
        score = await get_ms_ssim_score(await original_image.read(), await distorted_image.read())
        return ScoreOutSchema(score=score)
    except Exception as e:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=str(e))
