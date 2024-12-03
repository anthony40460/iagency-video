from fastapi import APIRouter, HTTPException
from ..models.video import VideoRequest, VideoResponse
from ..services.huggingface_service import HuggingFaceService
from datetime import datetime
import uuid

router = APIRouter()
huggingface_service = HuggingFaceService()

@router.post("/generate", response_model=VideoResponse)
async def generate_video(request: VideoRequest):
    try:
        video_data = await huggingface_service.generate_video(
            prompt=request.prompt,
            duration=request.duration,
            resolution=request.resolution,
            style=request.style
        )
        
        return VideoResponse(
            id=str(uuid.uuid4()),
            status="completed",
            video_url=video_data.get("video_url"),
            created_at=datetime.now(),
            prompt=request.prompt,
            duration=request.duration,
            resolution=request.resolution
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))