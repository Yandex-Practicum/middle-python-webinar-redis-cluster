import uvicorn
from fastapi import FastAPI

import url_shortener.src.config as config
from url_shortener.src.repositories import url_repository
from url_shortener.src.routers import short_url_router


app = FastAPI()


@app.on_event("startup")
async def startup():
    await url_repository.async_init()


@app.on_event("shutdown")
async def shutdown():
    await url_repository.async_stop()


@app.get("/")
async def root():
    """Just for check server"""
    return {"message": "Hello World"}


app.include_router(
    short_url_router,
    prefix="/short_url",
    tags=["short_url", "url"],
    responses={404: {"description": "Not found"}},
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.SERVICE_PORT)
