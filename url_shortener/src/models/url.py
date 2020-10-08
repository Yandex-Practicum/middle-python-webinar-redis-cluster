from pydantic import BaseModel, HttpUrl


class Url(BaseModel):
    full_path: HttpUrl
    redirect_path: HttpUrl
    url_key: str
