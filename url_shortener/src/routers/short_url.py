from fastapi import APIRouter, Path
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from ..config import URL_TTL_S, MIN_URL_LENGTH
from ..repositories import url_repository
from ..models import Url

router = APIRouter()


class InputUrl(BaseModel):
    url: str


@router.post("/")
async def create_url(url: InputUrl):
    return await url_repository.create_url(
        url.url, min_length=MIN_URL_LENGTH, ttl_s=URL_TTL_S
    )


@router.get("/{url_key}", response_model=Url)
async def fetch_url(
    url_key: str = Path(
        ...,
        min_length=4,
        max_length=50,
        title="Url key from POST /_short_url shortener",
    )
):
    return await url_repository.fetch_by_key(url_key)


@router.get("/r/{url_key}")
async def redirect_url(
    url_key: str = Path(
        ...,
        min_length=4,
        max_length=50,
        title="Url key from POST /_short_url shortener",
    )
):
    url_model = await url_repository.fetch_by_key(url_key)

    return RedirectResponse(url_model.full_path)
