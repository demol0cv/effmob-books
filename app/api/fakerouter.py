from fastapi import APIRouter


router = APIRouter(tags=["Fake"])

@router.get("/fake")
async def fill_fake_data():
    pass